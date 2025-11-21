import os
from app import create_app
from app.config import Config

# Validate configuration on startup
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    debug = Config.FLASK_ENV == 'development'
    
    app.run(host=host, port=port, debug=debug)

