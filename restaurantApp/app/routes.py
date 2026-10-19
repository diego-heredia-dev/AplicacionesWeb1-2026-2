from flask import Blueprint, render_template, request, redirect, url_for, flash
from .extensions import db
from .models import MenuItems, Categories

main = Blueprint('main', __name__)


# Página principal
@main.route('/')
def index():
    return render_template('index.html')


# READ: Listar platos
@main.route('/platos')
def listar_platos():
    platos = MenuItems.query.order_by(MenuItems.name).all()
    return render_template('platos.html', platos=platos)


# CREATE: Mostrar formulario y registrar plato
@main.route('/platos/crear', methods=['GET', 'POST'])
def crear_plato():
    categorias = Categories.query.order_by(Categories.name).all()

    if request.method == 'POST':
        nombre = request.form['name'].strip()
        descripcion = request.form['description'].strip()
        precio = request.form['price']
        categoria_id = request.form['category_id']

        if not nombre or not precio or not categoria_id:
            flash('Completa todos los campos obligatorios.', 'error')
            return render_template(
                'crear_plato.html',
                categorias=categorias
            )

        try:
            precio = float(precio)

            if precio <= 0:
                raise ValueError

            plato = MenuItems(
                name=nombre,
                description=descripcion or None,
                price=precio,
                category_id=categoria_id
            )

            db.session.add(plato)
            db.session.commit()

            flash('Plato registrado correctamente.', 'success')
            return redirect(url_for('main.listar_platos'))

        except ValueError:
            db.session.rollback()
            flash('El precio debe ser un número mayor que cero.', 'error')

        except Exception:
            db.session.rollback()
            flash('No se pudo registrar el plato. Comprueba los datos.', 'error')

    return render_template(
        'crear_plato.html',
        categorias=categorias
    )


# UPDATE: Editar plato
@main.route('/platos/editar/<uuid:plato_id>', methods=['GET', 'POST'])
def editar_plato(plato_id):
    plato = db.session.get(MenuItems, plato_id)

    if plato is None:
        return 'Plato no encontrado', 404

    categorias = Categories.query.order_by(Categories.name).all()

    if request.method == 'POST':
        nombre = request.form['name'].strip()
        descripcion = request.form['description'].strip()
        precio = request.form['price']
        categoria_id = request.form['category_id']

        if not nombre or not precio or not categoria_id:
            flash('Completa todos los campos obligatorios.', 'error')
            return render_template(
                'editar_plato.html',
                plato=plato,
                categorias=categorias
            )

        try:
            precio = float(precio)

            if precio <= 0:
                raise ValueError

            plato.name = nombre
            plato.description = descripcion or None
            plato.price = precio
            plato.category_id = categoria_id

            db.session.commit()

            flash('Plato actualizado correctamente.', 'success')
            return redirect(url_for('main.listar_platos'))

        except ValueError:
            db.session.rollback()
            flash('El precio debe ser un número mayor que cero.', 'error')

        except Exception:
            db.session.rollback()
            flash('No se pudo actualizar el plato. Comprueba los datos.', 'error')

    return render_template(
        'editar_plato.html',
        plato=plato,
        categorias=categorias
    )


# DELETE: Eliminar plato
@main.route('/platos/eliminar/<uuid:plato_id>', methods=['POST'])
def eliminar_plato(plato_id):
    plato = db.session.get(MenuItems, plato_id)

    if plato is None:
        return 'Plato no encontrado', 404

    try:
        db.session.delete(plato)
        db.session.commit()
        flash('Plato eliminado correctamente.', 'success')

    except Exception:
        db.session.rollback()
        flash(
            'No se pudo eliminar el plato. Puede estar asociado a un pedido.',
            'error'
        )

    return redirect(url_for('main.listar_platos'))