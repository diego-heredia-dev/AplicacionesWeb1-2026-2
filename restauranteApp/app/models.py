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