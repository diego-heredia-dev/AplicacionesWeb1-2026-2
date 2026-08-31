import os
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:abc@localhost:5432/example'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'

    menu_item_id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('gen_random_uuid()')
    )
    menu_item_id = db.Column(db.UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.String(120), nullable=False, unique=True)
    age = db.Column(db.Integer, db.CheckConstraint('age >= 0'))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f'<Person id={self.id} name={self.name}>'

    def format(self):
        """Convierte el objeto Python en un diccionario serializable a JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
        }



@app.route('/personas', methods=['GET'])
def listar_personas():
    """GET /personas  →  todas las personas.
       Acepta ?nombre=... para filtrar."""
    consulta = Person.query

    nombre = request.args.get('nombre')
    if nombre:
        consulta = consulta.filter(Person.name.ilike(f'%{nombre}%'))

    personas = consulta.order_by(Person.name).all()

    return jsonify({
        'success': True,
        'total': len(personas),
        'personas': [p.format() for p in personas]
    })


@app.route('/personas/<int:person_id>', methods=['GET'])
def obtener_persona(person_id):
    """GET /personas/3  →  una sola persona, o 404."""
    persona = Person.query.get(person_id)

    if persona is None:
        abort(404)

    return jsonify({'success': True, 'persona': persona.format()})


@app.route('/', methods=['GET'])
def salud():
    """GET /  →  comprobación rápida de que la conexión funciona."""
    total = Person.query.count()
    return jsonify({'status': 'ok', 'personas_registradas': total})


@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'success': False, 'error': 404,
                    'mensaje': 'recurso no encontrado'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
