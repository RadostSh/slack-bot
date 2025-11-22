import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-pro')
    
    # Parse Server/Back4App Configuration
    PARSE_APPLICATION_ID = os.getenv('PARSE_APPLICATION_ID')
    PARSE_REST_API_KEY = os.getenv('PARSE_REST_API_KEY')
    PARSE_SERVER_URL = os.getenv('PARSE_SERVER_URL')
    BACK4APP_INCIDENT_CLASS = 'IncidentMessage'
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    @staticmethod
    def validate():
        """Validate that all required environment variables are set."""
        required_vars = [
            'GEMINI_API_KEY',
            'PARSE_APPLICATION_ID',
            'PARSE_REST_API_KEY',
            'PARSE_SERVER_URL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

