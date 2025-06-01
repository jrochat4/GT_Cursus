from flask import Flask
from flask_login import LoginManager

# Placeholder for actual user loading function
# from .models import get_user_by_id

login_manager = LoginManager()
login_manager.login_view = 'main.login' # The route name for the login page
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_very_secret_key_for_flask_login' # Essential for sessions

    login_manager.init_app(app)

    # Import here to avoid circular dependency with login_manager
    from .models import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    from .main import routes as main_routes
    app.register_blueprint(main_routes.bp)

    # Make current_user available in all templates
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(current_user=current_user)

    return app
