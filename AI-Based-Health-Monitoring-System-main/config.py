"""
Configuration module for CarePulse Health Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # LLM Provider Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    
    # Anthropic Configuration
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Age Groups (for validation)
    AGE_GROUPS = [
        '0-2 years (Infant)',
        '3-5 years (Toddler)',
        '6-12 years (Child)',
        '13-17 years (Adolescent)',
        '18-64 years (Adult)',
        '65+ years (Senior)'
    ]
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'english': 'English',
        'spanish': 'Español (Spanish)',
        'french': 'Français (French)',
        'hindi': 'हिंदी (Hindi)',
        'bengali': 'বাংলা (Bengali)',
        'telugu': 'తెలుగు (Telugu)',
        'marathi': 'मराठी (Marathi)',
        'tamil': 'தமிழ் (Tamil)',
        'gujarati': 'ગુજરાતી (Gujarati)',
        'kannada': 'ಕನ್ನಡ (Kannada)',
        'malayalam': 'മലയാളം (Malayalam)',
        'punjabi': 'ਪੰਜਾਬੀ (Punjabi)',
        'odia': 'ଓଡ଼ିଆ (Odia)',
        'urdu': 'اردو (Urdu)',
        'assamese': 'অসমীয়া (Assamese)'
    }
    
    DEFAULT_LANGUAGE = 'english'
    
    @staticmethod
    def validate_config():
        """Validate that required API keys are present"""
        if Config.LLM_PROVIDER == 'openai' and not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")
        elif Config.LLM_PROVIDER == 'gemini' and not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER is 'gemini'")
        elif Config.LLM_PROVIDER == 'anthropic' and not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER is 'anthropic'")

