from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_login import LoginManager, current_user

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


class MyFlaskApp(Flask):
    def __init__(self, import_name):
        super().__init__(import_name)
        self.configure_app()
        self.configure_extensions()
        self.configure_blueprients()
        self.configure_context_processors()

    def configure_blueprients(self):
        from .routes import main
        from app.auth.routes import auth
        from app.admin.admin_route import admin
        for bp, prefix in [(main, None), (auth, "/auth"), (admin, "/admin")]:
            self.register_blueprint(bp, url_prefix=prefix)

    def configure_app(self):
        """Налаштовуємо конфігурацію застосунку."""
        self.config.from_object("app.config.Config")

    def configure_extensions(self):
        """Ініціалізуємо розширення (SQLAlchemy, Migrate)."""
        db.init_app(self)
        migrate.init_app(self, db, compare_type=True)
        login_manager.init_app(self)
        login_manager.login_view = "auth.login"

    def configure_context_processors(self):
        @self.context_processor
        def inject_user():
            return dict(current_user=current_user)


def create_app():
    return MyFlaskApp(__name__)
