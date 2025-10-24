# Portfolio Management Application

A comprehensive portfolio management application with real-time dashboard for portfolio managers and retail investors. Built with Python, Docker, Grafana, and integrated with yfinance API and OpenAI for intelligent insights.

## Features

### Core Functionality
- **Portfolio Management**: Create and manage multiple investment portfolios
- **Real-time Market Data**: Integration with yfinance API for live stock prices
- **Advanced Analytics**: Calculate key metrics including:
  - Alpha (excess returns)
  - Beta (market correlation)
  - Sharpe Ratio (risk-adjusted returns)
  - Portfolio volatility
  - Sector exposure analysis
- **AI-Powered Insights**: OpenAI integration for intelligent portfolio analysis
- **Interactive Dashboard**: Grafana-based visualization with real-time metrics
- **Performance Tracking**: Historical metrics and trend analysis

### Technical Features
- **Docker-based Architecture**: Fully containerized for easy deployment
- **RESTful API**: Flask backend with comprehensive endpoints
- **PostgreSQL Database**: Persistent data storage
- **Prometheus Metrics**: Application monitoring and metrics collection
- **Multi-user Support**: Portfolio manager and retail investor profiles

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: PostgreSQL 15
- **Market Data**: yfinance API
- **AI/ML**: OpenAI GPT-3.5
- **Visualization**: Grafana
- **Monitoring**: Prometheus
- **Containerization**: Docker, Docker Compose
- **Additional Libraries**: pandas, numpy, scipy

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (optional, for AI insights)
- Internet connection for market data

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Prittstick22/Encode_Project.git
cd Encode_Project
```

### 2. Configure Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key (optional):

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the Application

```bash
docker-compose up -d
```

This will start all services:
- Backend API: http://localhost:5000
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090
- PostgreSQL: localhost:5432

### 4. Access the Dashboard

1. Open Grafana at http://localhost:3000
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin`
3. Navigate to Dashboards → Portfolio Management Dashboard

## API Endpoints

### Portfolio Management

#### Create Portfolio
```bash
POST /api/portfolios
Content-Type: application/json

{
  "name": "My Investment Portfolio",
  "description": "Long-term growth portfolio",
  "user_type": "retail_investor"
}
```

#### Get All Portfolios
```bash
GET /api/portfolios
```

#### Get Portfolio Dashboard
```bash
GET /api/portfolios/{portfolio_id}/dashboard
```

Returns comprehensive portfolio data including:
- Current value and performance
- Holdings with gain/loss
- Alpha, Beta, Sharpe Ratio
- Sector exposure
- AI-generated insights

### Holdings Management

#### Add Holding
```bash
POST /api/portfolios/{portfolio_id}/holdings
Content-Type: application/json

{
  "ticker": "AAPL",
  "shares": 10,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-15T00:00:00"
}
```

#### Get Portfolio Holdings
```bash
GET /api/portfolios/{portfolio_id}/holdings
```

#### Update Holding
```bash
PUT /api/holdings/{holding_id}
Content-Type: application/json

{
  "shares": 15
}
```

#### Delete Holding
```bash
DELETE /api/holdings/{holding_id}
```

### Market Data

#### Get Stock Information
```bash
GET /api/stocks/{ticker}
```

#### Get AI Stock Analysis
```bash
GET /api/stocks/{ticker}/analysis
```

### Metrics

#### Get Historical Metrics
```bash
GET /api/portfolios/{portfolio_id}/metrics/history?limit=30
```

#### Prometheus Metrics
```bash
GET /metrics
```

## Example Usage

### Create a Sample Portfolio

```bash
# Create a portfolio
curl -X POST http://localhost:5000/api/portfolios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Growth Portfolio",
    "description": "Focus on technology stocks",
    "user_type": "portfolio_manager"
  }'

# Add holdings (replace {portfolio_id} with actual ID)
curl -X POST http://localhost:5000/api/portfolios/1/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "shares": 10,
    "purchase_price": 150.00,
    "purchase_date": "2024-01-15T00:00:00"
  }'

curl -X POST http://localhost:5000/api/portfolios/1/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "MSFT",
    "shares": 5,
    "purchase_price": 380.00,
    "purchase_date": "2024-01-15T00:00:00"
  }'

# Get dashboard
curl http://localhost:5000/api/portfolios/1/dashboard
```

## Project Structure

```
.
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main application
│   ├── models.py              # Database models
│   ├── services.py            # Portfolio analytics
│   ├── ai_service.py          # OpenAI integration
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container
├── grafana/                   # Grafana configuration
│   ├── provisioning/          # Auto-provisioning
│   │   ├── datasources/       # Data source configs
│   │   └── dashboards/        # Dashboard configs
│   └── dashboards/            # Dashboard JSON files
├── prometheus/                # Prometheus configuration
│   └── prometheus.yml         # Scrape configs
├── postgres/                  # PostgreSQL initialization
│   └── init.sql              # Database schema
├── docker-compose.yml         # Docker orchestration
├── .env.example              # Environment template
└── README.md                 # This file
```

## Key Metrics Explained

### Alpha
Measures excess return compared to the market benchmark (S&P 500). Positive alpha indicates outperformance.

### Beta
Measures portfolio volatility relative to the market. Beta > 1 means more volatile than market, Beta < 1 means less volatile.

### Sharpe Ratio
Risk-adjusted return metric. Higher values indicate better risk-adjusted performance. Values > 1 are generally considered good.

### Sector Exposure
Shows percentage allocation across different market sectors for diversification analysis.

## Development

### Running Tests

```bash
cd backend
python -m pytest
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### Stopping Services

```bash
docker-compose down
```

### Rebuilding After Changes

```bash
docker-compose up -d --build
```

## Troubleshooting

### Backend Service Won't Start
- Check if PostgreSQL is healthy: `docker-compose ps`
- View backend logs: `docker-compose logs backend`
- Ensure port 5000 is not in use

### Grafana Shows No Data
- Verify backend is running and accessible
- Check Prometheus is scraping metrics: http://localhost:9090/targets
- Ensure PostgreSQL connection in Grafana datasources

### Market Data Not Loading
- Check internet connection
- Verify ticker symbols are valid
- yfinance API may have rate limits

### OpenAI Insights Not Working
- Verify OPENAI_API_KEY is set in .env
- Check API key is valid and has credits
- Review backend logs for API errors

## Contributing

This project is for the Encode hackathon. Contributions are welcome!

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
