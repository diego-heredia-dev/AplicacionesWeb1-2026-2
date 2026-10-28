from flask import Flask

from .config import Config
from .extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from . import models
    from .routes import bp as lacarta_bp

    app.register_blueprint(lacarta_bp)
    # You may add severals blueprint when the app is bigger.
    return app