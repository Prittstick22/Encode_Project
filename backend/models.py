from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Portfolio(db.Model):
    """Portfolio model for storing portfolio information"""
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_type = db.Column(db.String(50))  # 'portfolio_manager' or 'retail_investor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    holdings = db.relationship('Holding', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'holdings_count': len(self.holdings)
        }


class Holding(db.Model):
    """Holding model for individual assets in a portfolio"""
    __tablename__ = 'holdings'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'ticker': self.ticker,
            'shares': self.shares,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PortfolioMetrics(db.Model):
    """Historical portfolio metrics"""
    __tablename__ = 'portfolio_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    total_value = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    total_gain_loss = db.Column(db.Float)
    alpha = db.Column(db.Float)
    beta = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'date': self.date.isoformat() if self.date else None,
            'total_value': self.total_value,
            'total_cost': self.total_cost,
            'total_gain_loss': self.total_gain_loss,
            'alpha': self.alpha,
            'beta': self.beta,
            'sharpe_ratio': self.sharpe_ratio,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
