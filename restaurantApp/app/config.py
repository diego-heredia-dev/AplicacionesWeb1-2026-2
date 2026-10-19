import os
from dotenv import load_dotenv

load_dotenv() #Carga las variables definidas en el archvio .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") # clave que flask utiliza para funciones de seguridad
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace(
    "postgresql://", "postgresql+psycopg2://", 1) # Este codigo es mas largo de lo que deberia por problema de versines de psycogf o algo asi
    SQLALCHEMY_TRACK_MODIFICATIONS = False #desactiva el seguimiento de cambios