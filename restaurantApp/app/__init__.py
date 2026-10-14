from flask import Flask

from .config import Config
from .extensions import db, migrate
from .routes import main

#Application Factory
def create_app(config_class=Config):
    #Crea la aplicacion Flask
    app = Flask(__name__)

    #Carga la configuracion definida en config.py
    app.config.from_object(config_class)

    #conecta la extension SQLALCHEMY con la aplicacion
    db.init_app(app)
    #configura migrate para trabajar con la app y la db
    migrate.init_app(app, db)
    #Importar models y routes dentro de create_app() ayuda a evitar problemas derivados de importar módulos antes de que la aplicación y sus extensiones estén preparadas.
    from . import models
    from .routes import main
    #Flask incorpora las rutas main a la aplicacion
    app.register_blueprint(main)

    return app