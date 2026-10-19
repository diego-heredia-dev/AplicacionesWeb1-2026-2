from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



#Instancia para definir los modelos y consultar la base de datos
db = SQLAlchemy() 
#Instancia para gestioanr migraciones 
migrate = Migrate()