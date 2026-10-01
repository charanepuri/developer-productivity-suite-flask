from unittest import result

from flask import Flask, render_template

from config import Config

from app.extensions import (
    db,
    migrate,
    login_manager,
    csrf
)

from datetime import datetime

from app.seed import seed_database

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    @app.context_processor
    def inject_global_variables():
        return {
            "current_year": datetime.now().year
    }

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # Import models
    from app.models import (
        User,
        Category,
        Tool,
        Favorite,
        SearchHistory,
        SavedResult,
    )

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Main Blueprint
    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Register Authentication Blueprint
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Register Dashboard Blueprint
    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Register Tools Blueprint
    from app.tools import tools_bp
    app.register_blueprint(tools_bp)

    # Register User Blueprint
    from app.user import user_bp
    app.register_blueprint(user_bp)

    # Register API Blueprint
    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Register Admin Blueprint
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    # Error handlers
    register_error_handlers(app)
    
    @app.cli.command("seed")
    def seed():
        """Seed categories and developer tools."""
        result = seed_database()

        print(
            f"Seed completed: "
            f"{result['categories_created']} categories created, "
            f"{result['tools_created']} tools created."
        )
    
    return app


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "errors/404.html"
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template(
            "errors/500.html"
        ), 500