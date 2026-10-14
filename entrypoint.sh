#indica que el archivo debe ejecutarse mediante el interprete de comandos sh
#!/bin/sh
#hace que el script termine si una instruccion falla
set -e
#aplica las migraciones pedientes de Flask-Migrate a la base de datos
flask db upgrade
#Inicia gunicorn utilizando la configuracion de gunicorn.conf.py y la aplicacion que expusimos en wsgi.py
exec gunicorn --config gunicorn.conf.py wsgi:app