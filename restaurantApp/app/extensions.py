from flask_sqlachemy import SQLALCHEMY
from flask_migrate import Migrate

#Instancia para definir los modelos y consultar la base de datos
db = SQLALCHEMY() 
#Instancia para gestioanr migraciones 
migrate = Migrate()