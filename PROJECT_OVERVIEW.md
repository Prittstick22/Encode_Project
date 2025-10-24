# Project Overview

## Portfolio Management Application

A comprehensive, production-ready portfolio management application designed for portfolio managers and retail investors to track, analyze, and optimize their investment portfolios.

## Key Features

### 1. Real-Time Portfolio Tracking
- Track multiple portfolios simultaneously
- Real-time market data via yfinance API
- Current valuations and historical performance
- Gain/loss calculations

### 2. Advanced Analytics
- **Alpha**: Measures excess returns compared to market benchmark (S&P 500)
- **Beta**: Portfolio volatility relative to market
- **Sharpe Ratio**: Risk-adjusted return analysis
- **Volatility**: Standard deviation of returns
- **Sector Exposure**: Diversification analysis across sectors

### 3. AI-Powered Insights
- Integration with OpenAI GPT-3.5
- Automated portfolio analysis
- Investment recommendations
- Stock-specific analysis

### 4. Interactive Dashboard
- Grafana-based visualization
- Real-time metrics display
- Historical trend analysis
- Performance monitoring

### 5. RESTful API
- Complete CRUD operations for portfolios and holdings
- Market data endpoints
- Historical metrics retrieval
- AI insights generation

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                                 │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Web UI     │    │   Grafana    │    │   Postman    │     │
│  │   (Future)   │    │  Dashboard   │    │  API Client  │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                   │                     │              │
└─────────┼───────────────────┼─────────────────────┼─────────────┘
          │                   │                     │
          └───────────────────┼─────────────────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────────┐
│                     APPLICATION LAYER                             │
│                              │                                     │
│  ┌───────────────────────────▼──────────────────────────┐        │
│  │         Flask Backend API (Port 5000)                │        │
│  │                                                       │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │        │
│  │  │  Portfolio  │  │   Market    │  │     AI      │ │        │
│  │  │ Management  │  │    Data     │  │  Insights   │ │        │
│  │  │   Service   │  │   Service   │  │   Service   │ │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │        │
│  │                                                       │        │
│  │  ┌─────────────────────────────────────────────┐   │        │
│  │  │      Prometheus Metrics (Port 8000)         │   │        │
│  │  └─────────────────────────────────────────────┘   │        │
│  └───────────────────────────────────────────────────────┘      │
│                              │                                     │
└──────────────────────────────┼─────────────────────────────────────┘
                               │
┌──────────────────────────────┼─────────────────────────────────────┐
│                     DATA LAYER                                     │
│                              │                                     │
│  ┌───────────────────────────▼──────────────────────────┐        │
│  │      PostgreSQL Database (Port 5432)                 │        │
│  │                                                       │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │        │
│  │  │ Portfolios  │  │  Holdings   │  │   Metrics   │ │        │
│  │  │   Table     │  │   Table     │  │   Table     │ │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │        │
│  └───────────────────────────────────────────────────────┘      │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    MONITORING LAYER                               │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   Prometheus     │◄────────┤    Grafana       │              │
│  │  (Port 9090)     │         │   (Port 3000)    │              │
│  │  - Time Series   │         │  - Dashboards    │              │
│  │  - Metrics       │         │  - Visualization │              │
│  └──────────────────┘         └──────────────────┘              │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                                │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  yfinance API    │         │   OpenAI API     │              │
│  │  (Yahoo Finance) │         │   (GPT-3.5)      │              │
│  │  - Market Data   │         │  - AI Insights   │              │
│  │  - Stock Prices  │         │  - Analysis      │              │
│  └──────────────────┘         └──────────────────┘              │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 3.1.1
- **API Integration**: 
  - yfinance 0.2.32 (Market Data)
  - openai 1.3.5 (AI Insights)
- **Analytics**: pandas 2.1.3, numpy 1.26.2, scipy 1.11.4
- **Monitoring**: prometheus-client 0.19.0

### Database
- **PostgreSQL 15**: Relational data storage
- **Connection**: psycopg2-binary 2.9.9

### Visualization
- **Grafana**: Dashboard and metrics visualization
- **Prometheus**: Time-series metrics collection

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Data Models

### Portfolio
- id (Primary Key)
- name
- description
- user_type (portfolio_manager | retail_investor)
- created_at, updated_at
- Holdings (One-to-Many relationship)

### Holding
- id (Primary Key)
- portfolio_id (Foreign Key)
- ticker
- shares
- purchase_price
- purchase_date
- created_at, updated_at

### PortfolioMetrics
- id (Primary Key)
- portfolio_id (Foreign Key)
- date
- total_value
- total_cost
- total_gain_loss
- alpha, beta, sharpe_ratio
- created_at

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /api/portfolios | List all portfolios |
| POST | /api/portfolios | Create portfolio |
| GET | /api/portfolios/{id} | Get portfolio |
| PUT | /api/portfolios/{id} | Update portfolio |
| DELETE | /api/portfolios/{id} | Delete portfolio |
| GET | /api/portfolios/{id}/holdings | List holdings |
| POST | /api/portfolios/{id}/holdings | Add holding |
| GET | /api/holdings/{id} | Get holding |
| PUT | /api/holdings/{id} | Update holding |
| DELETE | /api/holdings/{id} | Delete holding |
| GET | /api/portfolios/{id}/dashboard | Full dashboard data |
| GET | /api/portfolios/{id}/metrics/history | Historical metrics |
| GET | /api/stocks/{ticker} | Stock information |
| GET | /api/stocks/{ticker}/analysis | AI stock analysis |
| GET | /metrics | Prometheus metrics |

## Metrics Calculations

### Alpha (Jensen's Alpha)
```
α = Rp - [Rf + β(Rm - Rf)]

Where:
- Rp = Portfolio return
- Rf = Risk-free rate (3% annual)
- β = Portfolio beta
- Rm = Market return (S&P 500)
```

### Beta
```
β = Cov(Rp, Rm) / Var(Rm)

Where:
- Cov(Rp, Rm) = Covariance between portfolio and market returns
- Var(Rm) = Variance of market returns
```

### Sharpe Ratio
```
Sharpe = (Rp - Rf) / σp * √252

Where:
- Rp = Portfolio return
- Rf = Risk-free rate
- σp = Portfolio standard deviation
- √252 = Annualization factor (trading days)
```

## Files Structure

```
Encode_Project/
├── backend/                      # Python Flask application
│   ├── app.py                   # Main application entry point
│   ├── models.py                # SQLAlchemy models
│   ├── services.py              # Portfolio analytics services
│   ├── ai_service.py            # OpenAI integration
│   ├── config.py                # Configuration management
│   ├── requirements.txt         # Python dependencies
│   ├── test_app.py             # Test suite
│   └── Dockerfile              # Backend container definition
├── grafana/                     # Grafana configuration
│   ├── dashboards/             # Dashboard JSON definitions
│   └── provisioning/           # Auto-provisioning configs
├── prometheus/                  # Prometheus configuration
│   └── prometheus.yml          # Scrape configurations
├── postgres/                    # PostgreSQL initialization
│   └── init.sql                # Database schema
├── docker-compose.yml          # Multi-container orchestration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── API_DOCUMENTATION.md        # API reference
├── DEPLOYMENT.md               # Deployment guide
├── QUICKSTART.md              # Quick start guide
├── SECURITY.md                # Security guidelines
├── CONTRIBUTING.md            # Contribution guide
├── LICENSE                    # MIT License
├── Makefile                   # Convenient commands
├── setup.sh                   # Setup script
├── load_sample_data.sh        # Sample data loader
└── postman_collection.json    # Postman API collection
```

## Use Cases

### For Portfolio Managers
- Manage multiple client portfolios
- Track performance metrics
- Generate reports and insights
- Monitor risk exposure
- Compare portfolio performance

### For Retail Investors
- Track personal investments
- Understand portfolio risk
- Get AI-powered insights
- Monitor market performance
- Make informed decisions

## Getting Started

See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

## Documentation

- **[README.md](README.md)**: Main documentation and features
- **[QUICKSTART.md](QUICKSTART.md)**: Quick setup guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**: Complete API reference
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Production deployment guide
- **[SECURITY.md](SECURITY.md)**: Security best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines

## Future Enhancements

- User authentication and authorization
- Web-based frontend UI
- Mobile application
- Additional data sources (Alpha Vantage, IEX Cloud)
- More analytics (VaR, Sortino Ratio, etc.)
- Portfolio rebalancing recommendations
- Tax optimization tools
- Social trading features
- Email/SMS notifications
- Export to PDF/Excel

## Support

- GitHub Issues: For bug reports and feature requests
- Documentation: Comprehensive guides included
- Sample Data: Load demo portfolios with `./load_sample_data.sh`

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

Built for the Encode hackathon with a focus on:
- Collaborative development (Docker)
- Modern architecture
- Production readiness
- Comprehensive documentation
- Best practices

---

**Ready to manage your portfolio like a pro!** 🚀📈💼
