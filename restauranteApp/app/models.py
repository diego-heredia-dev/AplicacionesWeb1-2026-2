from .extensions import db


class Restaurante(db.Model):
    __tablename__ = "carta_restaurante"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(30))

    platos = db.relationship(
        "Plato",
        backref="restaurante",
        cascade="all, delete-orphan",
    )


class Plato(db.Model):
    __tablename__ = "carta_plato"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)

    restaurante_id = db.Column(
        db.Integer,
        db.ForeignKey("carta_restaurante.id", ondelete="CASCADE"),
        nullable=False,
    )


class Pedido(db.Model):
    __tablename__ = "carta_pedido"

    id = db.Column(db.BigInteger, primary_key=True)
    cliente = db.Column(db.String(255), nullable=False)
    restaurante_id = db.Column(
        db.Integer,
        db.ForeignKey("carta_restaurante.id"),
        nullable=False,
    )
    estado = db.Column(
        db.String(20),
        nullable=False,
        default="pendiente",
    )
    fecha = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
    )
    total = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    restaurante = db.relationship("Restaurante")
    items = db.relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan",
    )


class ItemPedido(db.Model):
    __tablename__ = "carta_itempedido"

    id = db.Column(db.BigInteger, primary_key=True)
    pedido_id = db.Column(
        db.BigInteger,
        db.ForeignKey("carta_pedido.id", ondelete="CASCADE"),
        nullable=False,
    )
    plato_id = db.Column(
        db.Integer,
        db.ForeignKey("carta_plato.id"),
        nullable=False,
    )
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    pedido = db.relationship(
        "Pedido",
        back_populates="items",
    )
    plato = db.relationship("Plato")
