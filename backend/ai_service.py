import openai
import os
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AIInsightsService:
    """Service for generating AI-powered portfolio insights using OpenAI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_portfolio_insights(self, portfolio_data: Dict) -> str:
        """Generate AI insights for portfolio"""
        if not self.api_key:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        try:
            # Prepare portfolio summary
            holdings_summary = []
            for holding in portfolio_data.get('holdings', []):
                holdings_summary.append(
                    f"- {holding['ticker']}: {holding['shares']} shares, "
                    f"Current Value: ${holding['current_value']:.2f}, "
                    f"Gain/Loss: {holding['gain_loss_pct']:.2f}%"
                )
            
            metrics = portfolio_data.get('metrics', {})
            
            prompt = f"""
As a financial advisor, analyze the following portfolio and provide key insights:

Portfolio Overview:
- Total Value: ${portfolio_data.get('total_value', 0):.2f}
- Total Cost Basis: ${portfolio_data.get('total_cost', 0):.2f}
- Total Gain/Loss: ${portfolio_data.get('total_gain_loss', 0):.2f} ({portfolio_data.get('total_gain_loss_pct', 0):.2f}%)

Holdings:
{chr(10).join(holdings_summary)}

Performance Metrics:
- Alpha: {metrics.get('alpha', 0):.4f}
- Beta: {metrics.get('beta', 1):.4f}
- Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.4f}
- Volatility: {metrics.get('volatility', 0):.2%}
- Portfolio Return: {metrics.get('portfolio_return', 0):.2%}

Sector Exposure:
{self._format_sector_exposure(portfolio_data.get('sector_exposure', {}))}

Provide:
1. Portfolio health assessment
2. Risk analysis based on beta and volatility
3. Performance evaluation using alpha and Sharpe ratio
4. Diversification recommendations
5. Key actionable insights

Keep the response concise and actionable (max 300 words).
"""
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert financial advisor specializing in portfolio analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating AI insights: {e}")
            return f"Unable to generate AI insights: {str(e)}"
    
    def generate_stock_analysis(self, ticker: str, stock_info: Dict) -> str:
        """Generate AI analysis for individual stock"""
        if not self.api_key:
            return "OpenAI API key not configured."
        
        try:
            prompt = f"""
Provide a brief analysis of {ticker}:
- Company: {stock_info.get('longName', ticker)}
- Sector: {stock_info.get('sector', 'N/A')}
- Industry: {stock_info.get('industry', 'N/A')}
- Market Cap: ${stock_info.get('marketCap', 0):,}
- PE Ratio: {stock_info.get('trailingPE', 'N/A')}
- 52 Week High: ${stock_info.get('fiftyTwoWeekHigh', 0):.2f}
- 52 Week Low: ${stock_info.get('fiftyTwoWeekLow', 0):.2f}

Provide a concise analysis (max 150 words) covering:
1. Company overview
2. Current valuation
3. Key considerations for investors
"""
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing stock analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating stock analysis: {e}")
            return f"Unable to generate analysis: {str(e)}"
    
    def _format_sector_exposure(self, sector_exposure: Dict) -> str:
        """Format sector exposure for prompt"""
        if not sector_exposure:
            return "No sector data available"
        
        formatted = []
        for sector, percentage in sorted(sector_exposure.items(), key=lambda x: x[1], reverse=True):
            formatted.append(f"- {sector}: {percentage:.2f}%")
        
        return '\n'.join(formatted)
