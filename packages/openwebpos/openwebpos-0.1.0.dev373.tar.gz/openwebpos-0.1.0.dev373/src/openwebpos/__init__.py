import os

from flask import Flask

from .extensions import db, login_manager, csrf
from .models.user import User
from .utils.money import cents_to_dollars
from .blueprints import core_bp


def create_app():
    """
    Create the Flask app instance.

    Returns:
        Flask: Flask app instance.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)

    # Default configuration
    app.config.from_object('config.settings')

    # Override default configuration
    app.config.from_envvar('APPLICATION_SETTINGS', silent=True)

    @app.context_processor
    def utility_processor():
        def format_currency(value):
            """
            Format currency. Converts cents to dollars.
            """
            return '${:,.2f}'.format(cents_to_dollars(value))

        def format_phone(value):
            """
            Format phone number.
            """
            return '({}) {}-{}'.format(value[:3], value[3:6], value[6:])

        return dict(format_currency=format_currency, format_phone=format_phone)

    # Initialize extensions
    load_extensions(app)

    # Register blueprints
    app.register_blueprint(core_bp)

    return app


def load_extensions(app):
    """
    Load extensions.

    Args:
        app (Flask): Flask app instance.
    """
    if app.config.get('DB_CONFIGURED'):
        # Only initialize extensions if database is configured
        db.init_app(app)

        with app.app_context():
            db.create_all()

        login_manager.init_app(app)
        login_manager.login_view = 'route.login'

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.filter_by(id=user_id).first()
    csrf.init_app(app)
