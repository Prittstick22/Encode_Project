# Quick Start Guide

Get the Portfolio Management Application running in under 5 minutes!

## Prerequisites Check

Before starting, verify you have:
- ✅ Docker installed: `docker --version`
- ✅ Docker Compose installed: `docker-compose --version`

If not installed, visit: https://docs.docker.com/get-docker/

## Installation Steps

### Step 1: Get the Code
```bash
git clone https://github.com/Prittstick22/Encode_Project.git
cd Encode_Project
```

### Step 2: Configure (Optional)
```bash
cp .env.example .env
# Edit .env to add your OpenAI API key (optional for AI insights)
nano .env  # or use your preferred editor
```

### Step 3: Start the Application
```bash
./setup.sh
```

Or manually:
```bash
docker-compose up -d
```

### Step 4: Wait for Services
The application takes about 30-60 seconds to fully start. Check status:
```bash
docker-compose ps
```

All services should show "Up" status.

## Access Your Application

### Grafana Dashboard
1. Open: http://localhost:3000
2. Login: `admin` / `admin`
3. Go to: Dashboards → Portfolio Management Dashboard

### Backend API
- API Base URL: http://localhost:5000
- Health Check: http://localhost:5000/health
- API Docs: See API_DOCUMENTATION.md

### Prometheus
- Metrics: http://localhost:9090

## Create Your First Portfolio

### Using cURL:

1. **Create a Portfolio**
```bash
curl -X POST http://localhost:5000/api/portfolios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Portfolio",
    "description": "Getting started with portfolio management",
    "user_type": "retail_investor"
  }'
```

Save the `id` from the response (e.g., `1`).

2. **Add Some Holdings**
```bash
# Apple Stock
curl -X POST http://localhost:5000/api/portfolios/1/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "shares": 10,
    "purchase_price": 150.00,
    "purchase_date": "2024-01-15T00:00:00"
  }'

# Microsoft Stock
curl -X POST http://localhost:5000/api/portfolios/1/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "MSFT",
    "shares": 5,
    "purchase_price": 380.00,
    "purchase_date": "2024-01-15T00:00:00"
  }'

# Google Stock
curl -X POST http://localhost:5000/api/portfolios/1/holdings \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "GOOGL",
    "shares": 3,
    "purchase_price": 140.00,
    "purchase_date": "2024-01-15T00:00:00"
  }'
```

3. **View Your Dashboard**
```bash
curl http://localhost:5000/api/portfolios/1/dashboard | jq
```

Or open in browser: http://localhost:5000/api/portfolios/1/dashboard

### Using Postman:

1. Import `postman_collection.json` into Postman
2. Use the pre-configured requests
3. Start with "Create Portfolio" request
4. Then use "Add Holding" requests
5. View results with "Get Portfolio Dashboard"

## View in Grafana

After creating portfolios and holdings:

1. Go to http://localhost:3000
2. Login with admin/admin
3. Navigate to Dashboards → Portfolio Management Dashboard
4. You'll see:
   - Total portfolio value
   - Gain/Loss
   - Alpha over time
   - Beta over time
   - Portfolio value history
   - Sharpe ratio
   - API metrics

## What's Next?

### Explore the API
- Check out `API_DOCUMENTATION.md` for all endpoints
- Try different stock tickers
- Create multiple portfolios
- View AI-generated insights

### Monitor Performance
- Watch Prometheus metrics at http://localhost:9090
- Create custom Grafana dashboards
- Track API performance

### Customize
- Add your own stocks
- Adjust dashboard visualizations
- Modify metrics calculations

## Common Commands

**View Logs:**
```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just database
docker-compose logs -f postgres
```

**Restart Services:**
```bash
docker-compose restart
```

**Stop Everything:**
```bash
docker-compose down
```

**Stop and Remove Data:**
```bash
docker-compose down -v
```

## Troubleshooting

### Can't Connect to Services
```bash
# Check if services are running
docker-compose ps

# Check if ports are in use
netstat -tlnp | grep -E '3000|5000|5432|9090'

# Restart services
docker-compose restart
```

### Backend Errors
```bash
# View backend logs
docker-compose logs backend

# Check database connection
docker-compose exec postgres pg_isready -U portfolio_user

# Restart backend
docker-compose restart backend
```

### No Data in Grafana
```bash
# Verify backend metrics
curl http://localhost:5000/metrics

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify database has data
docker-compose exec postgres psql -U portfolio_user -d portfolio_db -c "SELECT COUNT(*) FROM portfolios;"
```

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Create portfolio
PORTFOLIO_ID=$(curl -s -X POST http://localhost:5000/api/portfolios \
  -H "Content-Type: application/json" \
  -d '{"name": "Tech Portfolio", "user_type": "retail_investor"}' \
  | jq -r '.id')

echo "Created portfolio with ID: $PORTFOLIO_ID"

# 2. Add multiple holdings
for ticker in AAPL MSFT GOOGL AMZN TSLA; do
  curl -X POST http://localhost:5000/api/portfolios/$PORTFOLIO_ID/holdings \
    -H "Content-Type: application/json" \
    -d "{
      \"ticker\": \"$ticker\",
      \"shares\": 10,
      \"purchase_price\": 150.00,
      \"purchase_date\": \"2024-01-15T00:00:00\"
    }"
  echo "Added $ticker"
done

# 3. View dashboard
curl http://localhost:5000/api/portfolios/$PORTFOLIO_ID/dashboard | jq

# 4. Get AI insights
curl http://localhost:5000/api/portfolios/$PORTFOLIO_ID/dashboard | jq '.ai_insights'
```

## Learning Resources

- **API Documentation**: `API_DOCUMENTATION.md`
- **Deployment Guide**: `DEPLOYMENT.md`
- **Full README**: `README.md`
- **Postman Collection**: `postman_collection.json`

## Getting Help

If you run into issues:
1. Check the logs: `docker-compose logs -f`
2. Review the documentation
3. Open an issue on GitHub

## Next Steps

- ✅ Set up OpenAI API key for AI insights
- ✅ Create custom Grafana dashboards
- ✅ Explore different stock portfolios
- ✅ Monitor portfolio performance over time
- ✅ Deploy to production (see DEPLOYMENT.md)

Enjoy managing your portfolio! 🚀📈
