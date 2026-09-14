CREATE TABLE restaurantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    ciudad VARCHAR(80) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30)
);

CREATE TABLE platos(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    restaurante_id INTEGER NOT NULL,

    CONSTRAINT fk_plato_restaurante
        FOREIGN KEY (restaurante_id)
        REFERENCES restaurantes(id)
        ON DELETE CASCADE
);

INSERT INTO restaurantes (nombre, ciudad, direccion, telefono)
VALUES
    ('La Casa del Sabor', 'Santa Cruz', 'Av. San Martín #123', '70012345'),
    ('Sabores de Bolivia', 'La Paz', 'Calle Illampu #456', '70023456'),
    ('El Buen Plato', 'Cochabamba', 'Av. América #789', '70034567');

INSERT INTO platos (nombre, precio, disponible, restaurante_id)
VALUES
    ('Majadito', 35.00, TRUE, 1),
    ('Silpancho', 40.00, TRUE, 1),
    ('Sopa de Maní', 30.00, FALSE, 1),
    ('Pique Macho', 45.00, TRUE, 2),
    ('Fricasé', 38.00, TRUE, 2),
    ('Chairo', 32.00, TRUE, 2),
    ('Silpancho Cochabambino', 42.00, TRUE, 3),
    ('Pique Macho Especial', 50.00, FALSE, 3);