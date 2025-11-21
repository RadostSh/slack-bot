from flask import Flask
from app.config import Config


def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    from app.routes import incident_bp
    app.register_blueprint(incident_bp)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

