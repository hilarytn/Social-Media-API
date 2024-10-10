from flask import Flask
from extensions import db, jwt, migrate
from resources.auth import auth_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)