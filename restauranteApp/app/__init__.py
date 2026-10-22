from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config["BEHIND_PROXY"]:
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

    required = (
        "SECRET_KEY",
        "AUTH0_DOMAIN",
        "AUTH0_CLIENT_ID",
        "AUTH0_CLIENT_SECRET",
        "AUTH0_AUDIENCE",
    )

    for key in required:
        if not app.config.get(key):
            raise RuntimeError(f"Falta configurar la variable {key}.")

    db.init_app(app)

    from . import models  # noqa: F401
    from .auth import current_user
    from .auth.errors import AuthError
    from .auth.oauth import init_auth0
    from .auth.routes import bp as auth_bp
    from .auth.tokens import jwks_client
    from .routes import bp as main_bp

    init_auth0(app)
    app.extensions["auth0_jwks"] = jwks_client(
        app.config["AUTH0_DOMAIN"]
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_current_user():
        return {"current_user": current_user()}

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return {"error": error.message}, error.status_code

    return app
