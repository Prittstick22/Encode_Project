from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging

from config import Config
from models import db, Portfolio, Holding, PortfolioMetrics
from services import MarketDataService, PortfolioAnalytics
from ai_service import AIInsightsService
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Initialize services
market_data_service = MarketDataService()
portfolio_analytics = PortfolioAnalytics(market_data_service)
ai_insights_service = AIInsightsService(app.config.get('OPENAI_API_KEY'))

# Prometheus metrics
request_count = Counter('portfolio_requests_total', 'Total request count', ['method', 'endpoint', 'status'])
request_duration = Histogram('portfolio_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
portfolio_value = Gauge('portfolio_total_value', 'Total portfolio value', ['portfolio_id'])

# Add Prometheus middleware
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.before_request
def before_request():
    request.start_time = datetime.utcnow()


@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = (datetime.utcnow() - request.start_time).total_seconds()
        request_duration.labels(request.method, request.endpoint or 'unknown').observe(duration)
        request_count.labels(request.method, request.endpoint or 'unknown', response.status_code).inc()
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


@app.route('/api/portfolios', methods=['GET', 'POST'])
def portfolios():
    """Get all portfolios or create a new one"""
    if request.method == 'GET':
        portfolios = Portfolio.query.all()
        return jsonify([p.to_dict() for p in portfolios])
    
    elif request.method == 'POST':
        data = request.json
        portfolio = Portfolio(
            name=data.get('name'),
            description=data.get('description'),
            user_type=data.get('user_type', 'retail_investor')
        )
        db.session.add(portfolio)
        db.session.commit()
        logger.info(f"Created portfolio: {portfolio.id}")
        return jsonify(portfolio.to_dict()), 201


@app.route('/api/portfolios/<int:portfolio_id>', methods=['GET', 'PUT', 'DELETE'])
def portfolio_detail(portfolio_id):
    """Get, update, or delete a specific portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    if request.method == 'GET':
        return jsonify(portfolio.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        if 'name' in data:
            portfolio.name = data['name']
        if 'description' in data:
            portfolio.description = data['description']
        if 'user_type' in data:
            portfolio.user_type = data['user_type']
        
        db.session.commit()
        logger.info(f"Updated portfolio: {portfolio_id}")
        return jsonify(portfolio.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(portfolio)
        db.session.commit()
        logger.info(f"Deleted portfolio: {portfolio_id}")
        return '', 204


@app.route('/api/portfolios/<int:portfolio_id>/holdings', methods=['GET', 'POST'])
def portfolio_holdings(portfolio_id):
    """Get holdings or add a new holding to portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    if request.method == 'GET':
        holdings = Holding.query.filter_by(portfolio_id=portfolio_id).all()
        return jsonify([h.to_dict() for h in holdings])
    
    elif request.method == 'POST':
        data = request.json
        
        # Validate ticker
        ticker = data.get('ticker', '').upper()
        if not market_data_service.get_current_price(ticker):
            return jsonify({'error': f'Invalid ticker symbol: {ticker}'}), 400
        
        holding = Holding(
            portfolio_id=portfolio_id,
            ticker=ticker,
            shares=float(data.get('shares')),
            purchase_price=float(data.get('purchase_price')),
            purchase_date=datetime.fromisoformat(data.get('purchase_date'))
        )
        db.session.add(holding)
        db.session.commit()
        logger.info(f"Added holding {ticker} to portfolio {portfolio_id}")
        return jsonify(holding.to_dict()), 201


@app.route('/api/holdings/<int:holding_id>', methods=['GET', 'PUT', 'DELETE'])
def holding_detail(holding_id):
    """Get, update, or delete a specific holding"""
    holding = Holding.query.get_or_404(holding_id)
    
    if request.method == 'GET':
        return jsonify(holding.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        if 'shares' in data:
            holding.shares = float(data['shares'])
        if 'purchase_price' in data:
            holding.purchase_price = float(data['purchase_price'])
        
        db.session.commit()
        logger.info(f"Updated holding: {holding_id}")
        return jsonify(holding.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(holding)
        db.session.commit()
        logger.info(f"Deleted holding: {holding_id}")
        return '', 204


@app.route('/api/portfolios/<int:portfolio_id>/dashboard', methods=['GET'])
def portfolio_dashboard(portfolio_id):
    """Get comprehensive portfolio dashboard data"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    holdings = Holding.query.filter_by(portfolio_id=portfolio_id).all()
    
    if not holdings:
        return jsonify({
            'portfolio': portfolio.to_dict(),
            'summary': {
                'total_value': 0,
                'total_cost': 0,
                'total_gain_loss': 0,
                'total_gain_loss_pct': 0
            },
            'holdings': [],
            'metrics': {},
            'sector_exposure': {},
            'ai_insights': 'No holdings in portfolio yet.'
        })
    
    # Get holdings data
    holdings_data = [h.to_dict() for h in holdings]
    
    # Calculate portfolio value
    value_data = portfolio_analytics.calculate_portfolio_value(holdings_data)
    
    # Calculate metrics
    metrics = portfolio_analytics.calculate_portfolio_metrics(holdings_data)
    
    # Get sector exposure
    sector_exposure = portfolio_analytics.get_sector_exposure(holdings_data)
    
    # Update Prometheus metrics
    portfolio_value.labels(portfolio_id=portfolio_id).set(value_data['total_value'])
    
    # Store metrics in database
    portfolio_metric = PortfolioMetrics(
        portfolio_id=portfolio_id,
        date=datetime.utcnow(),
        total_value=value_data['total_value'],
        total_cost=value_data['total_cost'],
        total_gain_loss=value_data['total_gain_loss'],
        alpha=metrics.get('alpha'),
        beta=metrics.get('beta'),
        sharpe_ratio=metrics.get('sharpe_ratio')
    )
    db.session.add(portfolio_metric)
    db.session.commit()
    
    # Generate AI insights
    dashboard_data = {
        'total_value': value_data['total_value'],
        'total_cost': value_data['total_cost'],
        'total_gain_loss': value_data['total_gain_loss'],
        'total_gain_loss_pct': value_data['total_gain_loss_pct'],
        'holdings': value_data['holdings'],
        'metrics': metrics,
        'sector_exposure': sector_exposure
    }
    
    ai_insights = ai_insights_service.generate_portfolio_insights(dashboard_data)
    
    return jsonify({
        'portfolio': portfolio.to_dict(),
        'summary': {
            'total_value': value_data['total_value'],
            'total_cost': value_data['total_cost'],
            'total_gain_loss': value_data['total_gain_loss'],
            'total_gain_loss_pct': value_data['total_gain_loss_pct']
        },
        'holdings': value_data['holdings'],
        'metrics': metrics,
        'sector_exposure': sector_exposure,
        'ai_insights': ai_insights
    })


@app.route('/api/portfolios/<int:portfolio_id>/metrics/history', methods=['GET'])
def portfolio_metrics_history(portfolio_id):
    """Get historical metrics for portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    limit = request.args.get('limit', 30, type=int)
    metrics = PortfolioMetrics.query.filter_by(portfolio_id=portfolio_id)\
        .order_by(PortfolioMetrics.date.desc())\
        .limit(limit)\
        .all()
    
    return jsonify([m.to_dict() for m in metrics])


@app.route('/api/stocks/<ticker>', methods=['GET'])
def stock_info(ticker):
    """Get stock information and current price"""
    ticker = ticker.upper()
    
    current_price = market_data_service.get_current_price(ticker)
    if current_price is None:
        return jsonify({'error': 'Stock not found'}), 404
    
    info = market_data_service.get_stock_info(ticker)
    
    return jsonify({
        'ticker': ticker,
        'current_price': current_price,
        'info': info
    })


@app.route('/api/stocks/<ticker>/analysis', methods=['GET'])
def stock_analysis(ticker):
    """Get AI-powered stock analysis"""
    ticker = ticker.upper()
    
    info = market_data_service.get_stock_info(ticker)
    if not info:
        return jsonify({'error': 'Stock not found'}), 404
    
    analysis = ai_insights_service.generate_stock_analysis(ticker, info)
    
    return jsonify({
        'ticker': ticker,
        'analysis': analysis,
        'info': info
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
