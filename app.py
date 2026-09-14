import os

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Restaurante(db.Model):
    __tablename__ = "restaurantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(30))

    platos = db.relationship(
        "Plato",
        backref="restaurante",
        cascade="all, delete-orphan"
    )

class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)

    restaurante_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurantes.id", ondelete="CASCADE"),
        nullable=False
    )

@app.route("/")
def salud():
    total = Restaurante.query.count()

    return jsonify({
        "status": "ok",
        "restaurantes_registrados": total
    })

@app.route("/restaurantes")
def listar_restaurantes():
    restaurantes = Restaurante.query.order_by(Restaurante.nombre).all()

    return render_template(
        'restaurantes/index.html',
        restaurantes=restaurantes
    )

@app.route("/restaurantes/<int:restaurante_id>")
def detalle_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    return render_template(
        'restaurantes/detalle.html',
        restaurante=restaurante
    )

@app.route("/restaurantes/crear", methods=['GET', 'POST'])
def crear_restaurante():
    
    if request.method == 'GET':
        return render_template('restaurantes/crear.html')

    print("LLEGUÉ AL POST DE CREAR RESTAURANTE")
    
    nombre = request.form.get('nombre', '').strip()
    ciudad = request.form.get('ciudad', '').strip()
    direccion = request.form.get('direccion', '').strip()
    telefono = request.form.get('telefono', '').strip()

    if not nombre or not ciudad:
        flash('El nombre y la ciudad son obligatorios', 'error')
        return render_template('restaurantes/crear.html')

    restaurante = Restaurante(
        nombre=nombre,
        ciudad=ciudad,
        direccion=direccion or None,
        telefono=telefono or None
    )

    try:
        db.session.add(restaurante)
        db.session.commit()
        flash('Restaurante creado correctamente', 'success')
        return redirect(url_for('listar_restaurantes'))

    except Exception as e:
        db.session.rollback()
        print("ERROR AL CREAR RESTAURANTE:", e)
        flash('No se udo crear el restaurante', 'error')
    
    finally:
        db.session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)