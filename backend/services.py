import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MarketDataService:
    """Service for fetching market data using yfinance"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)
    
    def get_stock_data(self, ticker: str, period: str = '1y') -> Optional[pd.DataFrame]:
        """Fetch historical stock data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """Get current stock price"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='1d')
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            logger.error(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """Get stock information"""
        try:
            stock = yf.Ticker(ticker)
            return stock.info
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return None
    
    def get_market_index_data(self, index: str = '^GSPC', period: str = '1y') -> Optional[pd.DataFrame]:
        """Fetch market index data (default: S&P 500)"""
        return self.get_stock_data(index, period)


class PortfolioAnalytics:
    """Service for portfolio analytics calculations"""
    
    def __init__(self, market_data_service: MarketDataService):
        self.market_data = market_data_service
    
    def calculate_portfolio_value(self, holdings: List[Dict]) -> Dict:
        """Calculate current portfolio value"""
        total_value = 0
        total_cost = 0
        holding_details = []
        
        for holding in holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            purchase_price = holding['purchase_price']
            
            current_price = self.market_data.get_current_price(ticker)
            if current_price:
                current_value = shares * current_price
                cost_basis = shares * purchase_price
                gain_loss = current_value - cost_basis
                gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
                
                total_value += current_value
                total_cost += cost_basis
                
                holding_details.append({
                    'ticker': ticker,
                    'shares': shares,
                    'purchase_price': purchase_price,
                    'current_price': current_price,
                    'current_value': current_value,
                    'cost_basis': cost_basis,
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                })
        
        total_gain_loss = total_value - total_cost
        total_gain_loss_pct = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': total_gain_loss_pct,
            'holdings': holding_details
        }
    
    def calculate_beta(self, returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate portfolio beta relative to market"""
        try:
            if len(returns) < 2 or len(market_returns) < 2:
                return 1.0
            
            # Align the series
            aligned_data = pd.DataFrame({
                'returns': returns,
                'market': market_returns
            }).dropna()
            
            if len(aligned_data) < 2:
                return 1.0
            
            covariance = aligned_data['returns'].cov(aligned_data['market'])
            market_variance = aligned_data['market'].var()
            
            if market_variance == 0:
                return 1.0
            
            beta = covariance / market_variance
            return float(beta)
        except Exception as e:
            logger.error(f"Error calculating beta: {e}")
            return 1.0
    
    def calculate_alpha(self, portfolio_return: float, market_return: float, 
                       beta: float, risk_free_rate: float = 0.03) -> float:
        """Calculate portfolio alpha (Jensen's alpha)"""
        try:
            expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
            alpha = portfolio_return - expected_return
            return float(alpha)
        except Exception as e:
            logger.error(f"Error calculating alpha: {e}")
            return 0.0
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.03) -> float:
        """Calculate Sharpe ratio"""
        try:
            if len(returns) < 2:
                return 0.0
            
            excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
            sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
            return float(sharpe)
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def calculate_portfolio_metrics(self, holdings: List[Dict], period: str = '1y') -> Dict:
        """Calculate comprehensive portfolio metrics"""
        try:
            # Get portfolio returns
            portfolio_returns = []
            weights = []
            
            for holding in holdings:
                ticker = holding['ticker']
                shares = holding['shares']
                hist_data = self.market_data.get_stock_data(ticker, period)
                
                if hist_data is not None and not hist_data.empty:
                    returns = hist_data['Close'].pct_change().dropna()
                    portfolio_returns.append(returns)
                    
                    current_price = self.market_data.get_current_price(ticker)
                    if current_price:
                        weights.append(shares * current_price)
            
            if not portfolio_returns:
                return self._default_metrics()
            
            # Calculate weighted portfolio returns
            total_weight = sum(weights)
            weights = [w / total_weight for w in weights] if total_weight > 0 else [1/len(weights)] * len(weights)
            
            # Align all returns to common dates
            combined_returns = pd.DataFrame(portfolio_returns).T
            combined_returns = combined_returns.dropna()
            
            # Calculate weighted returns
            weighted_returns = (combined_returns * weights).sum(axis=1)
            
            # Get market returns (S&P 500)
            market_data = self.market_data.get_market_index_data('^GSPC', period)
            if market_data is not None and not market_data.empty:
                market_returns = market_data['Close'].pct_change().dropna()
            else:
                return self._default_metrics()
            
            # Calculate metrics
            beta = self.calculate_beta(weighted_returns, market_returns)
            
            portfolio_return = float((weighted_returns + 1).prod() - 1)
            market_return = float((market_returns + 1).prod() - 1)
            
            alpha = self.calculate_alpha(portfolio_return, market_return, beta)
            sharpe_ratio = self.calculate_sharpe_ratio(weighted_returns)
            
            # Calculate volatility
            volatility = float(weighted_returns.std() * np.sqrt(252))
            
            return {
                'alpha': alpha,
                'beta': beta,
                'sharpe_ratio': sharpe_ratio,
                'volatility': volatility,
                'portfolio_return': portfolio_return,
                'market_return': market_return
            }
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return self._default_metrics()
    
    def _default_metrics(self) -> Dict:
        """Return default metrics when calculation fails"""
        return {
            'alpha': 0.0,
            'beta': 1.0,
            'sharpe_ratio': 0.0,
            'volatility': 0.0,
            'portfolio_return': 0.0,
            'market_return': 0.0
        }
    
    def get_sector_exposure(self, holdings: List[Dict]) -> Dict:
        """Calculate sector exposure"""
        sector_exposure = {}
        total_value = 0
        
        for holding in holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            
            current_price = self.market_data.get_current_price(ticker)
            if current_price:
                value = shares * current_price
                total_value += value
                
                info = self.market_data.get_stock_info(ticker)
                if info and 'sector' in info:
                    sector = info['sector']
                    sector_exposure[sector] = sector_exposure.get(sector, 0) + value
        
        # Convert to percentages
        if total_value > 0:
            sector_exposure = {
                sector: (value / total_value * 100) 
                for sector, value in sector_exposure.items()
            }
        
        return sector_exposure
