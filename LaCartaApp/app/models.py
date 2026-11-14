from .extensions import db
from datetime import datetime, timezone

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

    empleados = db.relationship(
        "Empleado",
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

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(120), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurantes.id"), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    fecha = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    restaurante = db.relationship("Restaurante", backref="pedidos")
    items = db.relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")

class ItemPedido(db.Model):
    __tablename__ = "items_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    plato = db.relationship("Plato", backref="items_pedido")

class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(80), nullable=False)

    restaurante_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurantes.id", ondelete="CASCADE"),
        nullable=False
    )