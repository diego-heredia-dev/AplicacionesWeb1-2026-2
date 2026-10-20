from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,


from .extensions import db
from .models import Plato, Restaurante


bp = Blueprint("restaurantes", __name__)


@bp.route("/")
def salud():
    total = Restaurante.query.count()

    return jsonify({
        "status": "ok",
        "restaurantes_registrados": total,
    })


@bp.route("/restaurantes")
def listar_restaurantes():
    ciudad = request.args.get("ciudad", "").strip()

    query = Restaurante.query

    if ciudad:
        query = query.filter(
            Restaurante.ciudad.ilike(ciudad)
        )

    restaurantes = query.order_by(
        Restaurante.nombre
    ).all()

    return render_template(
        "restaurantes/index.html",
        restaurantes=restaurantes,
    )


@bp.route("/restaurantes/<int:restaurante_id>")
def detalle_restaurante(restaurante_id):
    restaurante = db.get_or_404(
        Restaurante,
        restaurante_id,
    )

    return render_template(
        "restaurantes/detalle.html",
        restaurante=restaurante,
    )


@bp.route("/restaurantes/crear", methods=["GET", "POST"])
def crear_restaurante():
    if request.method == "GET":
        return render_template("restaurantes/crear.html")

    nombre = request.form.get("nombre", "").strip()
    ciudad = request.form.get("ciudad", "").strip()
    direccion = request.form.get("direccion", "").strip()
    telefono = request.form.get("telefono", "").strip()

    if not nombre or not ciudad:
        flash("El nombre y la ciudad son obligatorios.", "error")
        return render_template("restaurantes/crear.html")

    restaurante = Restaurante(
        nombre=nombre,
        ciudad=ciudad,
        direccion=direccion or None,
        telefono=telefono or None,
    )

    try:
        db.session.add(restaurante)
        db.session.commit()
        flash("Restaurante creado correctamente.", "success",)
        return redirect(url_for("restaurantes.listar_restaurantes"))

    except Exception:
        db.session.rollback()
        flash("No se pudo crear el restaurante.", "error")
        return render_template("restaurantes/crear.html")

    finally:
        db.session.close()

@bp.route("/restaurantes/<int:restaurante_id>/editar", methods=["GET", "POST"])
def editar_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    if request.method == "GET":
        return render_template("restaurantes/editar.html", restaurante=restaurante)

    nombre = request.form.get("nombre", "").strip()
    ciudad = request.form.get("ciudad", "").strip()
    direccion = request.form.get("direccion", "").strip()
    telefono = request.form.get("telefono", "").strip()

    if not nombre or not ciudad:
        flash("El nombre y la ciudad son obligatorios.", "error")
        return render_template("restaurantes/editar.html", restaurante=restaurante)

    restaurante.nombre = nombre
    restaurante.ciudad = ciudad
    restaurante.direccion = direccion or None
    restaurante.telefono = telefono or None

    try:
        db.session.commit()
        flash("Restaurante actualizado correctamente.", "success")
        return redirect(url_for("restaurantes.detalle_restaurante", restaurante_id=restaurante.id))

    except Exception:
        db.session.rollback()
        flash("No se pudo actualizar el restaurante.", "error")
        return render_template("restaurantes/editar.html", restaurante=restaurante)

    finally:
        db.session.close()


@bp.route(
    "/restaurantes/<int:restaurante_id>/eliminar",
    methods=["POST"],
)
def eliminar_restaurante(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    try:
        db.session.delete(restaurante)
        db.session.commit()
        flash("Restaurante eliminado correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo eliminar el restaurante.", "error")

    return redirect(
        url_for("restaurantes.listar_restaurantes")
    )


@bp.route(
    "/restaurantes/<int:restaurante_id>/platos",
    methods=["POST"],
)
def agregar_plato(restaurante_id):
    restaurante = db.get_or_404(Restaurante, restaurante_id)

    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", "").strip()
    disponible = request.form.get("disponible") == "on"

    if not nombre or not precio:
        flash("El nombre y el precio son obligatorios.", "error")

        return redirect(
            url_for("restaurantes.detalle_restaurante", restaurante_id=restaurante.id)
        )

    try:
        precio = float(precio)
        if precio <= 0:
            raise ValueError

    except ValueError:
        flash("El precio debe ser un número mayor que 0.", "error")

        return redirect(
            url_for("restaurantes.detalle_restaurante", restaurante_id=restaurante.id)
        )

    finally:
        db.session.close()

    plato = Plato(
        nombre=nombre,
        precio=precio,
        disponible=disponible,
        restaurante_id=restaurante.id,
    )

    try:
        db.session.add(plato)
        db.session.commit()
        flash("Plato agregado correctamente.", "success")

    except Exception:
        db.session.rollback()
        flash("No se pudo agregar el plato.", "error")

    return redirect(
        url_for("restaurantes.detalle_restaurante", restaurante_id=restaurante.id)
    )