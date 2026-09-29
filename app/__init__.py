from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # CSRF protection
    csrf.init_app(app)

    # Flask-Login will be initialized later
    # after the User model and user_loader are created.

    # Register blueprints
    from app.main import main_bp

    app.register_blueprint(main_bp)

    return app