from flask import Blueprint, render_template
#Blueprint permite organizar las rutas en grupos
#Esta linea crea un grupo de rutas llamado main
main = Blueprint('main', __name__)

#define la ruta principal de nuestra app
@main.route('/')
def index():
    return render_template('index.html')