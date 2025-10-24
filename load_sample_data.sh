#!/bin/bash

# Sample Data Loader
# This script populates the application with sample portfolio data

set -e

BASE_URL="http://localhost:5000"

echo "========================================="
echo "Loading Sample Portfolio Data"
echo "========================================="
echo ""

# Check if backend is running
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "Error: Backend is not running at $BASE_URL"
    echo "Please start the application first: docker-compose up -d"
    exit 1
fi

echo "✓ Backend is running"
echo ""

# Create Portfolio 1: Tech Growth Portfolio
echo "Creating Tech Growth Portfolio..."
PORTFOLIO1=$(curl -s -X POST "$BASE_URL/api/portfolios" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Growth Portfolio",
    "description": "Focus on high-growth technology companies",
    "user_type": "portfolio_manager"
  }' | jq -r '.id')

echo "✓ Created portfolio ID: $PORTFOLIO1"

# Add holdings to Portfolio 1
echo "Adding tech stock holdings..."
holdings1=(
  '{"ticker": "AAPL", "shares": 50, "purchase_price": 150.00, "purchase_date": "2024-01-15T00:00:00"}'
  '{"ticker": "MSFT", "shares": 30, "purchase_price": 380.00, "purchase_date": "2024-01-15T00:00:00"}'
  '{"ticker": "GOOGL", "shares": 25, "purchase_price": 140.00, "purchase_date": "2024-01-15T00:00:00"}'
  '{"ticker": "NVDA", "shares": 20, "purchase_price": 500.00, "purchase_date": "2024-01-20T00:00:00"}'
  '{"ticker": "META", "shares": 15, "purchase_price": 350.00, "purchase_date": "2024-01-20T00:00:00"}'
)

for holding in "${holdings1[@]}"; do
  ticker=$(echo "$holding" | jq -r '.ticker')
  curl -s -X POST "$BASE_URL/api/portfolios/$PORTFOLIO1/holdings" \
    -H "Content-Type: application/json" \
    -d "$holding" > /dev/null
  echo "  ✓ Added $ticker"
done

# Create Portfolio 2: Diversified Index Portfolio
echo ""
echo "Creating Diversified Index Portfolio..."
PORTFOLIO2=$(curl -s -X POST "$BASE_URL/api/portfolios" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Diversified Index Portfolio",
    "description": "Broad market exposure with blue-chip stocks",
    "user_type": "retail_investor"
  }' | jq -r '.id')

echo "✓ Created portfolio ID: $PORTFOLIO2"

# Add holdings to Portfolio 2
echo "Adding diversified holdings..."
holdings2=(
  '{"ticker": "VOO", "shares": 100, "purchase_price": 420.00, "purchase_date": "2023-12-01T00:00:00"}'
  '{"ticker": "BND", "shares": 200, "purchase_price": 75.00, "purchase_date": "2023-12-01T00:00:00"}'
  '{"ticker": "VTI", "shares": 50, "purchase_price": 240.00, "purchase_date": "2023-12-01T00:00:00"}'
  '{"ticker": "AAPL", "shares": 10, "purchase_price": 145.00, "purchase_date": "2023-12-15T00:00:00"}'
  '{"ticker": "JNJ", "shares": 20, "purchase_price": 160.00, "purchase_date": "2024-01-10T00:00:00"}'
)

for holding in "${holdings2[@]}"; do
  ticker=$(echo "$holding" | jq -r '.ticker')
  curl -s -X POST "$BASE_URL/api/portfolios/$PORTFOLIO2/holdings" \
    -H "Content-Type: application/json" \
    -d "$holding" > /dev/null
  echo "  ✓ Added $ticker"
done

# Create Portfolio 3: Growth & Income Portfolio
echo ""
echo "Creating Growth & Income Portfolio..."
PORTFOLIO3=$(curl -s -X POST "$BASE_URL/api/portfolios" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Growth & Income Portfolio",
    "description": "Balance of growth stocks and dividend payers",
    "user_type": "retail_investor"
  }' | jq -r '.id')

echo "✓ Created portfolio ID: $PORTFOLIO3"

# Add holdings to Portfolio 3
echo "Adding growth and income holdings..."
holdings3=(
  '{"ticker": "AMZN", "shares": 15, "purchase_price": 145.00, "purchase_date": "2023-11-01T00:00:00"}'
  '{"ticker": "TSLA", "shares": 20, "purchase_price": 240.00, "purchase_date": "2023-11-15T00:00:00"}'
  '{"ticker": "KO", "shares": 100, "purchase_price": 58.00, "purchase_date": "2023-12-01T00:00:00"}'
  '{"ticker": "PG", "shares": 30, "purchase_price": 155.00, "purchase_date": "2024-01-05T00:00:00"}'
  '{"ticker": "JPM", "shares": 25, "purchase_price": 170.00, "purchase_date": "2024-01-15T00:00:00"}'
)

for holding in "${holdings3[@]}"; do
  ticker=$(echo "$holding" | jq -r '.ticker')
  curl -s -X POST "$BASE_URL/api/portfolios/$PORTFOLIO3/holdings" \
    -H "Content-Type: application/json" \
    -d "$holding" > /dev/null
  echo "  ✓ Added $ticker"
done

echo ""
echo "========================================="
echo "Sample Data Loaded Successfully!"
echo "========================================="
echo ""
echo "Created 3 portfolios with multiple holdings"
echo ""
echo "View your portfolios:"
echo "  Portfolio 1 (Tech Growth): curl $BASE_URL/api/portfolios/$PORTFOLIO1/dashboard | jq"
echo "  Portfolio 2 (Diversified): curl $BASE_URL/api/portfolios/$PORTFOLIO2/dashboard | jq"
echo "  Portfolio 3 (Growth & Income): curl $BASE_URL/api/portfolios/$PORTFOLIO3/dashboard | jq"
echo ""
echo "All portfolios: curl $BASE_URL/api/portfolios | jq"
echo ""
echo "Next steps:"
echo "  1. View portfolios in Grafana: http://localhost:3000"
echo "  2. Explore the API endpoints"
echo "  3. Check portfolio metrics and AI insights"
echo ""
