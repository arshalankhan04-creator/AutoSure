"""
Application Configuration
Centralized configuration settings for AutoSure
"""

import os
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'AutoSure')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'car_service_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Business settings
    COMPANY_NAME = os.getenv('COMPANY_NAME', 'Easy Ride Auto Service')
    COMPANY_ADDRESS = os.getenv('COMPANY_ADDRESS', 'Gujarat, India')
    COMPANY_PHONE = os.getenv('COMPANY_PHONE', '+91 98765 43210')
    COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'info@easyride.com')
    
    # Tax settings (using Decimal for financial precision)
    TAX_RATE = Decimal(os.getenv('TAX_RATE', '0.18'))  # 18% GST for India
    TAX_NAME = os.getenv('TAX_NAME', 'GST')
    
    # Invoice settings
    INVOICE_PREFIX = os.getenv('INVOICE_PREFIX', 'INV')
    ORDER_PREFIX = os.getenv('ORDER_PREFIX', 'WO')  # Work Order prefix
    PAYMENT_TERMS_DAYS = int(os.getenv('PAYMENT_TERMS_DAYS', '30'))
    
    # Currency settings
    CURRENCY_SYMBOL = os.getenv('CURRENCY_SYMBOL', '₹')
    CURRENCY_CODE = os.getenv('CURRENCY_CODE', 'INR')
    
    # Labor rate settings (using Decimal for financial precision)
    DEFAULT_LABOR_RATE = Decimal(os.getenv('DEFAULT_LABOR_RATE', '500.00'))
    
    # Session settings
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    
    # Inventory settings
    LOW_STOCK_THRESHOLD = int(os.getenv('LOW_STOCK_THRESHOLD', '10'))
    
    # Service catalog categories
    INVENTORY_CATEGORIES = [
        'Electrical',
        'Exterior',
        'Filters',
        'Brakes',
        'Ignition',
        'Fluids'
    ]
    
    # Category code mapping for auto-generation
    CATEGORY_CODE_MAP = {
        'Electrical': 'ELC',
        'Exterior': 'EXT',
        'Filters': 'FLT',
        'Brakes': 'BRK',
        'Ignition': 'IGN',
        'Fluids': 'OIL'
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    DB_NAME = os.getenv('DB_NAME', 'car_service_test_db')
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])


# Create a global config instance
app_config = get_config()
