# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### Portfolios

#### GET /api/portfolios
Get all portfolios.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Tech Growth Portfolio",
    "description": "Focus on technology stocks",
    "user_type": "portfolio_manager",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00",
    "holdings_count": 5
  }
]
```

#### POST /api/portfolios
Create a new portfolio.

**Request Body:**
```json
{
  "name": "My Portfolio",
  "description": "Long-term investment portfolio",
  "user_type": "retail_investor"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "name": "My Portfolio",
  "description": "Long-term investment portfolio",
  "user_type": "retail_investor",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00",
  "holdings_count": 0
}
```

#### GET /api/portfolios/{portfolio_id}
Get a specific portfolio by ID.

**Response:**
```json
{
  "id": 1,
  "name": "My Portfolio",
  "description": "Long-term investment portfolio",
  "user_type": "retail_investor",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00",
  "holdings_count": 3
}
```

#### PUT /api/portfolios/{portfolio_id}
Update a portfolio.

**Request Body:**
```json
{
  "name": "Updated Portfolio Name",
  "description": "New description"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Portfolio Name",
  "description": "New description",
  "user_type": "retail_investor",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T11:00:00",
  "holdings_count": 3
}
```

#### DELETE /api/portfolios/{portfolio_id}
Delete a portfolio.

**Response:** (204 No Content)

---

### Holdings

#### GET /api/portfolios/{portfolio_id}/holdings
Get all holdings for a portfolio.

**Response:**
```json
[
  {
    "id": 1,
    "portfolio_id": 1,
    "ticker": "AAPL",
    "shares": 10,
    "purchase_price": 150.00,
    "purchase_date": "2024-01-15T00:00:00",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00"
  }
]
```

#### POST /api/portfolios/{portfolio_id}/holdings
Add a new holding to a portfolio.

**Request Body:**
```json
{
  "ticker": "AAPL",
  "shares": 10,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-15T00:00:00"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "portfolio_id": 1,
  "ticker": "AAPL",
  "shares": 10,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-15T00:00:00",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

#### GET /api/holdings/{holding_id}
Get a specific holding.

**Response:**
```json
{
  "id": 1,
  "portfolio_id": 1,
  "ticker": "AAPL",
  "shares": 10,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-15T00:00:00",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

#### PUT /api/holdings/{holding_id}
Update a holding.

**Request Body:**
```json
{
  "shares": 15,
  "purchase_price": 145.00
}
```

**Response:**
```json
{
  "id": 1,
  "portfolio_id": 1,
  "ticker": "AAPL",
  "shares": 15,
  "purchase_price": 145.00,
  "purchase_date": "2024-01-15T00:00:00",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

#### DELETE /api/holdings/{holding_id}
Delete a holding.

**Response:** (204 No Content)

---

### Dashboard

#### GET /api/portfolios/{portfolio_id}/dashboard
Get comprehensive dashboard data for a portfolio.

**Response:**
```json
{
  "portfolio": {
    "id": 1,
    "name": "Tech Growth Portfolio",
    "description": "Focus on technology stocks",
    "user_type": "portfolio_manager",
    "created_at": "2024-01-15T10:00:00",
    "updated_at": "2024-01-15T10:00:00",
    "holdings_count": 3
  },
  "summary": {
    "total_value": 5250.00,
    "total_cost": 5000.00,
    "total_gain_loss": 250.00,
    "total_gain_loss_pct": 5.0
  },
  "holdings": [
    {
      "ticker": "AAPL",
      "shares": 10,
      "purchase_price": 150.00,
      "current_price": 175.00,
      "current_value": 1750.00,
      "cost_basis": 1500.00,
      "gain_loss": 250.00,
      "gain_loss_pct": 16.67
    }
  ],
  "metrics": {
    "alpha": 0.0234,
    "beta": 1.15,
    "sharpe_ratio": 1.45,
    "volatility": 0.18,
    "portfolio_return": 0.05,
    "market_return": 0.03
  },
  "sector_exposure": {
    "Technology": 60.0,
    "Healthcare": 25.0,
    "Finance": 15.0
  },
  "ai_insights": "Your portfolio shows strong performance with positive alpha..."
}
```

---

### Metrics

#### GET /api/portfolios/{portfolio_id}/metrics/history
Get historical metrics for a portfolio.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 30)

**Response:**
```json
[
  {
    "id": 1,
    "portfolio_id": 1,
    "date": "2024-01-15T10:00:00",
    "total_value": 5250.00,
    "total_cost": 5000.00,
    "total_gain_loss": 250.00,
    "alpha": 0.0234,
    "beta": 1.15,
    "sharpe_ratio": 1.45,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

### Stocks

#### GET /api/stocks/{ticker}
Get current stock information.

**Example:** GET /api/stocks/AAPL

**Response:**
```json
{
  "ticker": "AAPL",
  "current_price": 175.50,
  "info": {
    "longName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "marketCap": 2750000000000,
    "trailingPE": 28.5,
    "fiftyTwoWeekHigh": 199.62,
    "fiftyTwoWeekLow": 164.08
  }
}
```

#### GET /api/stocks/{ticker}/analysis
Get AI-powered stock analysis.

**Example:** GET /api/stocks/AAPL/analysis

**Response:**
```json
{
  "ticker": "AAPL",
  "analysis": "Apple Inc. is a technology giant with strong fundamentals...",
  "info": {
    "longName": "Apple Inc.",
    "sector": "Technology",
    "marketCap": 2750000000000
  }
}
```

---

### Prometheus Metrics

#### GET /metrics
Get Prometheus metrics for monitoring.

**Response:** (Prometheus text format)
```
# HELP portfolio_requests_total Total request count
# TYPE portfolio_requests_total counter
portfolio_requests_total{method="GET",endpoint="/api/portfolios",status="200"} 42

# HELP portfolio_request_duration_seconds Request duration
# TYPE portfolio_request_duration_seconds histogram
...
```

---

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "error": "Invalid ticker symbol: XYZ"
}
```

### 404 Not Found
```json
{
  "error": "Not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Data Types

### User Types
- `portfolio_manager`: Professional portfolio manager
- `retail_investor`: Individual retail investor

### Ticker Symbols
Valid stock ticker symbols (e.g., AAPL, MSFT, GOOGL)

### Date Format
ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

Example: `2024-01-15T10:30:00`
