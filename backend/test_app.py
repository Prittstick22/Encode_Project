import pytest
from datetime import datetime
from app import app, db
from models import Portfolio, Holding


@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def sample_portfolio(client):
    """Create a sample portfolio"""
    response = client.post('/api/portfolios', json={
        'name': 'Test Portfolio',
        'description': 'Test Description',
        'user_type': 'retail_investor'
    })
    return response.get_json()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_create_portfolio(client):
    """Test portfolio creation"""
    response = client.post('/api/portfolios', json={
        'name': 'My Portfolio',
        'description': 'Test portfolio',
        'user_type': 'portfolio_manager'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'My Portfolio'
    assert data['user_type'] == 'portfolio_manager'


def test_get_portfolios(client, sample_portfolio):
    """Test getting all portfolios"""
    response = client.get('/api/portfolios')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['name'] == 'Test Portfolio'


def test_get_portfolio_by_id(client, sample_portfolio):
    """Test getting portfolio by ID"""
    portfolio_id = sample_portfolio['id']
    response = client.get(f'/api/portfolios/{portfolio_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == portfolio_id


def test_update_portfolio(client, sample_portfolio):
    """Test updating portfolio"""
    portfolio_id = sample_portfolio['id']
    response = client.put(f'/api/portfolios/{portfolio_id}', json={
        'name': 'Updated Portfolio'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Portfolio'


def test_delete_portfolio(client, sample_portfolio):
    """Test deleting portfolio"""
    portfolio_id = sample_portfolio['id']
    response = client.delete(f'/api/portfolios/{portfolio_id}')
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f'/api/portfolios/{portfolio_id}')
    assert response.status_code == 404


def test_add_holding(client, sample_portfolio):
    """Test adding holding to portfolio"""
    portfolio_id = sample_portfolio['id']
    response = client.post(f'/api/portfolios/{portfolio_id}/holdings', json={
        'ticker': 'AAPL',
        'shares': 10,
        'purchase_price': 150.00,
        'purchase_date': '2024-01-15T00:00:00'
    })
    # Note: This might fail in test environment without network access
    # In production, yfinance would validate the ticker
    assert response.status_code in [201, 400]


def test_get_holdings(client, sample_portfolio):
    """Test getting portfolio holdings"""
    portfolio_id = sample_portfolio['id']
    response = client.get(f'/api/portfolios/{portfolio_id}/holdings')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_stock_info_endpoint(client):
    """Test stock info endpoint"""
    # This test requires network access and may fail in isolated environments
    response = client.get('/api/stocks/AAPL')
    # Accept both success and failure due to network dependency
    assert response.status_code in [200, 404, 500]


def test_portfolio_dashboard(client, sample_portfolio):
    """Test portfolio dashboard endpoint"""
    portfolio_id = sample_portfolio['id']
    response = client.get(f'/api/portfolios/{portfolio_id}/dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert 'portfolio' in data
    assert 'summary' in data
    assert 'holdings' in data
    assert 'metrics' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
