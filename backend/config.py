import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://portfolio_user:portfolio_pass@postgres:5432/portfolio_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Flask
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Prometheus
    PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', '8000'))
