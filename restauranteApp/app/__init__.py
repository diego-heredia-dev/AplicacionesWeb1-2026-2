from flask import Flask

from .config import Config
from .extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Inicializar las extensiones.
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar los modelos en la metadata de SQLAlchemy.
    from . import models  # noqa: F401

    # Registrar las rutas.
    from .routes import bp as main_bp

    app.register_blueprint(main_bp)

    return app