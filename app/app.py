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
    ciudad = request.args.get('ciudad', '').strip()

    query = Restaurante.query

    #Agrega un filtro al query
    if ciudad:
        query = query.filter(
            Restaurante.ciudad.ilike(ciudad)
        )

    restaurantes = query.order_by(Restaurante.nombre).all()

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

    except Exception:
        db.session.rollback()
        flash('No se pudo crear el restaurante', 'error')
        return render_template('restaurantes/crear.html')
    
    finally:
        db.session.close()

@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET', 'POST'])
def editar_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    if request.method == 'GET':
        return render_template(
            'restaurantes/editar.html',
            restaurante=restaurante)

    nombre = request.form.get('nombre', '').strip()
    ciudad = request.form.get('ciudad', '').strip()
    direccion = request.form.get('direccion', '').strip()
    telefono = request.form.get('telefono', '').strip()

    if not nombre or not ciudad:
        flash('El nombre y ciudad son obligatorios', 'error')
        return render_template(
            'restaurantes/editar.html',
            restaurante=restaurante
        )

    restaurante.nombre = nombre
    restaurante.ciudad = ciudad 
    restaurante.direccion = direccion
    restaurante.telefono = telefono

    try:
        db.session.commit()
        flash('Restaurante actualizado correctamente', 'success')
        return redirect(
            url_for('detalle_restaurante', restaurante_id=restaurante.id)
        )

    except Exception:
        db.session.rollback()
        flash('No se pudo actualizar el restaurante', 'error')
        return render_template(
            'restaurantes/editar.html',
            restaurante=restaurante
        )

    finally:
        db.session.close()

@app.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
def eliminar_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    try:
        db.session.delete(restaurante)
        db.session.commit()
        flash('Restaurante eliminado correctamente', 'success')
        return redirect(url_for('listar_restaurantes'))

    except Exception as e:
        db.session.rollback()
        print('Error al eliminar:', e)
        flash('No se pudo eliminar el restaurante', 'error')
        return redirect(url_for('listar_restaurantes'))

    finally:
        db.session.close()

@app.route('/restaurantes/<int:restaurante_id>/platos', methods=['POST'])
def agregar_plato(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    nombre = request.form.get('nombre', '').strip()
    precio = request.form.get('precio', '').strip()
    disponible = request.form.get('disponible') == 'on' #Es una comparación que convierte ese resultado en un booleano:

    if not nombre or not precio:
        flash('El nombre y el precio son obligatorios', 'error')
        return redirect(
            url_for('detalle_restaurante', restaurante_id=restaurante.id)
        )

    try:
        precio = float(precio)

        if precio <= 0:
            raise ValueError

    except ValueError:
        flash('El precio debe ser mayor que 0', 'error')
        return redirect(
            url_for('detalle_restaurante', restaurante_id=restaurante.id)
        )

    plato = Plato(
        nombre=nombre,
        precio=precio,
        disponible=disponible,
        restaurante_id=restaurante.id
    )

    try:
        db.session.add(plato)
        db.session.commit()

        flash('Plato agregado correctamente', 'success')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))

    except Exception:
        db.session.rollback()
        flash('No se pudo agregar el plato', 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante.id))

    finally:
        db.session.close()


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(error):
    db.session.rollback()

    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)