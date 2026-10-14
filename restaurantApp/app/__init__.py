from flask import Flask

from .config import Config
from .extensions import db, migrate

#Application Factory
def create_app():
    #Crea la aplicacion Flask
    app = Flask(__name__)

    #Carga la configuracion definida en config.py
    app.config.from_object(Config)

    #conecta la extension SQLALCHEMY con la aplicacion
    db.init_app(app)
    #configura migrate para trabajar con la app y la db
    migrate.init_app(app, db)

    return app