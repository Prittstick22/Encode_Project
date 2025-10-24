-- Initialize Portfolio Database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_holdings_ticker ON holdings(ticker);
CREATE INDEX IF NOT EXISTS idx_portfolio_metrics_portfolio_id ON portfolio_metrics(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_metrics_date ON portfolio_metrics(date);

-- Create a view for portfolio summary
CREATE OR REPLACE VIEW portfolio_summary AS
SELECT 
    p.id,
    p.name,
    p.user_type,
    COUNT(h.id) as total_holdings,
    p.created_at,
    p.updated_at
FROM portfolios p
LEFT JOIN holdings h ON p.id = h.portfolio_id
GROUP BY p.id, p.name, p.user_type, p.created_at, p.updated_at;
