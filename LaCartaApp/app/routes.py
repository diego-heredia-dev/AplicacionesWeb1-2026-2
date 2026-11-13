from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify, session, abort

from .extensions import db
from .models import Restaurante, Plato, Pedido, ItemPedido
from .auth.decorators import requires_auth
from decimal import Decimal, InvalidOperation

bp = Blueprint("lacarta", __name__)

@bp.route("/")
def salud():        
    total = Restaurante.query.count()

    return jsonify({
        "status": "ok",
        "restaurantes_registrados": total
    })

@bp.route("/restaurantes")
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

@bp.route("/restaurantes/<int:restaurante_id>")
def detalle_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    return render_template(
        'restaurantes/detalle.html',
        restaurante=restaurante
    )

@bp.route("/restaurantes/crear", methods=['GET', 'POST'])
@requires_auth("write:carta")
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
        return redirect(url_for('.listar_restaurantes'))

    except Exception:
        db.session.rollback()
        flash('No se pudo crear el restaurante', 'error')
        return render_template('restaurantes/crear.html')
    

@bp.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET', 'POST'])
@requires_auth("write:carta")
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
            url_for('.detalle_restaurante', restaurante_id=restaurante.id)
        )

    except Exception:
        db.session.rollback()
        flash('No se pudo actualizar el restaurante', 'error')
        return render_template(
            'restaurantes/editar.html',
            restaurante=restaurante
        )

@bp.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
@requires_auth("delete:carta")
def eliminar_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    try:
        db.session.delete(restaurante)
        db.session.commit()
        flash('Restaurante eliminado correctamente', 'success')
        return redirect(url_for('.listar_restaurantes'))

    except Exception as e:
        db.session.rollback()
        print('Error al eliminar:', e)
        flash('No se pudo eliminar el restaurante', 'error')
        return redirect(url_for('.listar_restaurantes'))

@bp.route('/restaurantes/<int:restaurante_id>/platos', methods=['POST'])
@requires_auth("write:carta")
def agregar_plato(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    nombre = request.form.get('nombre', '').strip()
    precio = request.form.get('precio', '').strip()
    disponible = request.form.get('disponible') == 'on' #Es una comparación que convierte ese resultado en un booleano:

    if not nombre or not precio:
        flash('El nombre y el precio son obligatorios', 'error')
        return redirect(
            url_for('.detalle_restaurante', restaurante_id=restaurante.id)
        )

    try:
        precio = float(precio)

        if precio <= 0:
            raise ValueError

    except ValueError:
        flash('El precio debe ser mayor que 0', 'error')
        return redirect(
            url_for('.detalle_restaurante', restaurante_id=restaurante.id)
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
        return redirect(url_for('.detalle_restaurante', restaurante_id=restaurante.id))

    except Exception:
        db.session.rollback()
        flash('No se pudo agregar el plato', 'error')
        return redirect(url_for('.detalle_restaurante', restaurante_id=restaurante.id))


@bp.route(
    "/restaurantes/<int:restaurante_id>/pedidos",
    methods=["POST"]
)
@requires_auth("create:pedidos")
def crear_pedido(restaurante_id):
    cliente_id = session["user"]["sub"]

    restaurante = db.get_or_404(Restaurante, restaurante_id)
    restaurante_id = restaurante.id

    items_pedido = []
    total = Decimal("0.00")

    try:
        for key, value in request.form.items():
            if not key.startswith("plato_"):
                continue

            plato_id = int(key.replace("plato_", ""))
            cantidad = int(value)

            if cantidad < 0:
                raise ValueError

            if cantidad == 0:
                continue

            plato = Plato.query.filter_by(
                id=plato_id,
                restaurante_id=restaurante.id,
                disponible=True
            ).first()

            if not plato:
                raise ValueError

            subtotal = plato.precio * cantidad
            total += subtotal

            items_pedido.append({
                "plato": plato,
                "cantidad": cantidad,
                "precio": plato.precio
            })

        if not items_pedido:
            raise ValueError

    except (ValueError, InvalidOperation):
        flash("El pedido contiene datos inválidos.", "error")
        return redirect(
            url_for(
                ".detalle_restaurante",
                restaurante_id=restaurante.id
            )
        )

    pedido = Pedido(
        cliente=cliente_id,
        restaurante_id=restaurante.id,
        estado="pendiente",
        total=total
    )

    try:
        db.session.add(pedido)
        db.session.flush()

        for item in items_pedido:
            nuevo_item = ItemPedido(
                pedido_id=pedido.id,
                plato_id=item["plato"].id,
                cantidad=item["cantidad"],
                precio_unitario=item["precio"]
            )

            db.session.add(nuevo_item)

        db.session.commit()

        flash("¡Pedido realizado correctamente!", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo registrar el pedido.", "error")

    return redirect(
        url_for(".detalle_restaurante", restaurante_id=restaurante_id)
    )

@bp.route("/pedidos")
@requires_auth("read:mis-pedidos")
def mis_pedidos():
    cliente_id = session["user"]["sub"]

    pedidos = Pedido.query.filter_by(
        cliente=cliente_id
    ).order_by(
        Pedido.fecha.desc()
    ).all()

    return render_template(
        "pedidos/index.html",
        pedidos=pedidos
    )

@bp.route("/pedidos/<int:pedido_id>/cancelar", methods=["POST"])
@requires_auth("read:mis-pedidos")
def cancelar_pedido(pedido_id):
    cliente_id = session["user"]["sub"]

    pedido = Pedido.query.filter_by(
        id=pedido_id,
        cliente=cliente_id
    ).first_or_404()

    try:
        pedido.estado = "cancelado"
        db.session.commit()

        flash("Pedido cancelado correctamente.", "success")

    except Exception:
        db.session.rollback()

        flash("No se pudo cancelar el pedido.", "error")

    return redirect(url_for(".mis_pedidos"))

@bp.route("/cocina")
@requires_auth("read:pedidos")
def cola_cocina():
    estados_activos = [
        "pendiente",
        "en_preparacion",
        "listo"
    ]

    pedidos = Pedido.query.filter(
        Pedido.estado.in_(estados_activos)
    ).order_by(
        Pedido.fecha.asc()
    ).all()

    return render_template(
        "cocina/index.html",
        pedidos=pedidos
    )

@bp.route("/cocina/pedidos/<int:pedido_id>/avanzar", methods=["POST"])
@requires_auth("update:pedidos")
def avanzar_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    transiciones = {
        "pendiente": "en_preparacion",
        "en_preparacion": "listo",
        "listo": "entregado"
    }

    siguiente_estado = transiciones.get(pedido.estado)

    if not siguiente_estado:
        flash("Este pedido ya no puede avanzar de estado.", "error")
        return redirect(url_for(".cola_cocina"))

    try:
        pedido.estado = siguiente_estado
        db.session.commit()

        flash(
            f"El pedido #{pedido.id} ahora está: {siguiente_estado}.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo actualizar el estado del pedido.", "error")

    return redirect(url_for(".cola_cocina"))

@bp.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def error_interno(error):
    db.session.rollback()

    return render_template('500.html'), 500