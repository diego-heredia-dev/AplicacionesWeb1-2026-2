from flask import Flask

from .config import Config
from .extensions import db
from .auth.oauth import init_auth0

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    init_auth0(app)

    from . import models
    from .routes import bp as lacarta_bp

    app.register_blueprint(lacarta_bp)
    
    return app