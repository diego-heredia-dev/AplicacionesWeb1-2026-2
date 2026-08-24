CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA content;

CREATE TABLE content.customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) UNIQUE
);

CREATE TABLE content.employees (
    employee_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL
);

CREATE TABLE content.restaurant_tables (
    table_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_number INTEGER NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    available BOOLEAN NOT NULL
);

CREATE TABLE content.menu_items (
    menu_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    price NUMERIC(10,2) NOT NULL CHECK (price > 0),
    available BOOLEAN NOT NULL
);

CREATE TABLE content.reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    table_id UUID NOT NULL,
    reservation_date TIMESTAMP NOT NULL,
    party_size INTEGER NOT NULL CHECK (party_size > 0),
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES content.customers(customer_id),

    FOREIGN KEY (table_id)
        REFERENCES content.restaurant_tables(table_id)
);

CREATE TABLE content.orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID,
    employee_id UUID NOT NULL,
    table_id UUID,
    order_date TIMESTAMP NOT NULL,
    status VARCHAR(30) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount > 0),

    FOREIGN KEY (customer_id)
        REFERENCES content.customers(customer_id),

    FOREIGN KEY (employee_id)
        REFERENCES content.employees(employee_id),

    FOREIGN KEY (table_id)
        REFERENCES content.restaurant_tables(table_id)
);

CREATE TABLE content.order_items (
    order_id UUID NOT NULL,
    menu_item_id UUID NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price > 0),

    PRIMARY KEY (order_id, menu_item_id),

    FOREIGN KEY (order_id)
        REFERENCES content.orders(order_id),

    FOREIGN KEY (menu_item_id)
        REFERENCES content.menu_items(menu_item_id)
);

CREATE TABLE content.payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    payment_method VARCHAR(30) NOT NULL,
    payment_date TIMESTAMP NOT NULL,
    status VARCHAR(30) NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES content.orders(order_id)
);
