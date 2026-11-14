from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import db
from .auth.oauth import init_auth0
from .auth.decorators import has_permission


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1
    )

    db.init_app(app)
    init_auth0(app)

    from . import models
    from .routes import bp as lacarta_bp
    from .auth.routes import bp as auth_bp

    app.register_blueprint(lacarta_bp)
    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_permissions():
        return dict(has_permission=has_permission)

    return app