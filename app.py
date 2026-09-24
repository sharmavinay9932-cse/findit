import os
from flask import Flask
from flask_cors import CORS
from config.config import Config

from routes.auth_routes import auth_bp
from routes.item_routes import item_bp
from routes.match_routes import match_bp
from routes.user_routes import user_bp
from routes.frontend_routes import frontend_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Register Blueprints for API
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(item_bp, url_prefix='/api/items')
    app.register_blueprint(match_bp, url_prefix='/api/matches')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    from routes.claim_routes import claim_bp
    from routes.return_routes import return_bp
    app.register_blueprint(claim_bp, url_prefix='/api/claims')
    app.register_blueprint(return_bp, url_prefix='/api/returns')
    
    # Frontend Routes (serve HTML)
    app.register_blueprint(frontend_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
