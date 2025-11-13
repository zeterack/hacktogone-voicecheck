import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration centralisée de l'application"""
    
    # Mode mock
    USE_MOCK_SERVICES = os.getenv('USE_MOCK_SERVICES', 'True').lower() == 'true'
    
    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Blend AI (remplace Twilio)
    BLEND_API_KEY = os.getenv('BLEND_API_KEY', '')
    BLEND_ENDPOINT = os.getenv('BLEND_ENDPOINT', 'https://api.bland.ai/v1/calls')
    
    # Application
    APP_URL = os.getenv('APP_URL', 'http://localhost:8501')
    
    @classmethod
    def is_mock_mode(cls):
        """Détermine si on doit utiliser les services mock"""
        if cls.USE_MOCK_SERVICES:
            return True
        # Utiliser mock si les clés API Blend ou OpenAI sont manquantes
        if not cls.BLEND_API_KEY or not cls.OPENAI_API_KEY:
            return True
        return False
