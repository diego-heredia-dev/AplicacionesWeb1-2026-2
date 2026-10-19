import random
import sys

from pathlib import Path
from uuid import uuid4
from datetime import date, datetime, timedelta
from decimal import Decimal

# Permite importar la aplicación desde la carpeta raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import (
    Customers,
    Employees,
    RestaurantTables,
    Categories,
    MenuItems,
    Reservations,
    Orders,
    OrderItems,
    Payments,
    Users
)
from werkzeug.security import generate_password_hash


# ==========================================
# CONFIGURACIÓN
# ==========================================

random.seed(42)

CANTIDADES = {
    "customers": 1500,
    "employees": 100,
    "restaurant_tables": 50,
    "categories": 20,
    "menu_items": 300,
    "reservations": 1500,
    "orders": 1800,
    "order_items": 2500,
    "payments": 1600,
    "users": 630
}

NOMBRES = [
    "Carlos", "Maria", "Jose", "Ana", "Luis",
    "Lucia", "Miguel", "Sofia", "Diego", "Valeria",
    "Fernando", "Camila", "Javier", "Daniela", "Andres",
    "Gabriela", "Pablo", "Isabella", "Ricardo", "Paula"
]

APELLIDOS = [
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores",
    "Rivera", "Gomez", "Diaz", "Cruz", "Morales",
    "Ortiz", "Castro", "Vargas", "Rojas", "Mendoza"
]

NOMBRES_CATEGORIAS = [
    "Entradas", "Ensaladas", "Sopas", "Pastas",
    "Carnes", "Pollo", "Pescados", "Mariscos",
    "Hamburguesas", "Pizzas", "Sandwiches", "Guarniciones",
    "Comida tipica", "Comida internacional", "Postres",
    "Helados", "Bebidas frias", "Bebidas calientes",
    "Jugos naturales", "Especialidades"
]

NOMBRES_PLATOS = [
    "Pollo a la plancha", "Carne a la parrilla",
    "Pasta Alfredo", "Ensalada Cesar", "Sopa de verduras",
    "Hamburguesa clasica", "Pizza margarita",
    "Pescado al horno", "Arroz con pollo",
    "Lasaña de carne", "Milanesa de pollo",
    "Lomo salteado", "Papas fritas", "Pure de papas",
    "Brownie de chocolate", "Tarta de manzana",
    "Helado de vainilla", "Jugo de naranja",
    "Limonada natural", "Cafe americano",
    "Te de hierbas", "Sandwich de pollo",
    "Empanadas de carne", "Ravioles de queso",
    "Costillas a la BBQ", "Risotto de champiñones",
    "Ceviche", "Tacos de carne", "Flan casero",
    "Batido de frutilla"
]

app = create_app()


# ==========================================
# GENERACIÓN DE DATOS
# ==========================================

def generar_datos():
    # --------------------------------------
    # CUSTOMERS: 1500
    # --------------------------------------

    customers = []

    for i in range(CANTIDADES["customers"]):
        customer = Customers(
            customer_id=uuid4(),
            first_name=random.choice(NOMBRES),
            last_name=random.choice(APELLIDOS),
            email=f"cliente{i + 1}@example.com",
            phone=f"+5917{i:07d}"
        )

        customers.append(customer)

    # --------------------------------------
    # EMPLOYEES: 100
    # --------------------------------------

    employees = []

    roles = [
        "waiter",
        "cook",
        "manager",
        "cashier"
    ]

    for i in range(CANTIDADES["employees"]):
        employee = Employees(
            employee_id=uuid4(),
            first_name=random.choice(NOMBRES),
            last_name=random.choice(APELLIDOS),
            email=f"empleado{i + 1}@example.com",
            phone=f"+5916{i:07d}",
            role=random.choice(roles),
            hire_date=date.today() - timedelta(
                days=random.randint(30, 2500)
            )
        )

        employees.append(employee)

    # --------------------------------------
    # RESTAURANT TABLES: 50
    # --------------------------------------

    restaurant_tables = []

    for i in range(CANTIDADES["restaurant_tables"]):
        table = RestaurantTables(
            table_id=uuid4(),
            table_number=i + 1,
            capacity=random.choice([2, 2, 4, 4, 6, 8]),
            available=True
        )

        restaurant_tables.append(table)

    # --------------------------------------
    # CATEGORIES: 20
    # --------------------------------------

    categories = []

    for name in NOMBRES_CATEGORIAS:
        category = Categories(
            category_id=uuid4(),
            name=name,
            description=f"Categoria de {name.lower()}"
        )

        categories.append(category)

    # --------------------------------------
    # MENU ITEMS: 300
    # --------------------------------------

    menu_items = []

    for i in range(CANTIDADES["menu_items"]):
        base_name = NOMBRES_PLATOS[i % len(NOMBRES_PLATOS)]

        # El sufijo evita nombres duplicados
        name = f"{base_name} {i + 1:03d}"

        menu_item = MenuItems(
            menu_item_id=uuid4(),
            category_id=random.choice(categories).category_id,
            name=name,
            description=f"Plato de ejemplo numero {i + 1}",
            price=Decimal(
                str(round(random.uniform(10, 150), 2))
            ),
            available=random.choice([True, True, True, False])
        )

        menu_items.append(menu_item)

    # --------------------------------------
    # RESERVATIONS: 1500
    # --------------------------------------

    reservations = []

    for i in range(CANTIDADES["reservations"]):
        reservation = Reservations(
            reservation_id=uuid4(),
            customer_id=random.choice(customers).customer_id,
            table_id=random.choice(restaurant_tables).table_id,
            reservation_date=datetime.now() + timedelta(
                days=random.randint(-180, 90),
                hours=random.randint(0, 12)
            ),
            party_size=random.randint(1, 8),
            status=random.choice([
                "pending",
                "confirmed",
                "completed",
                "cancelled"
            ])
        )

        reservations.append(reservation)

    # --------------------------------------
    # ORDERS: 1800
    # --------------------------------------

    orders = []

    for i in range(CANTIDADES["orders"]):
        order = Orders(
            order_id=uuid4(),
            customer_id=(
                random.choice(customers).customer_id
                if random.random() < 0.8
                else None
            ),
            employee_id=random.choice(employees).employee_id,
            table_id=(
                random.choice(restaurant_tables).table_id
                if random.random() < 0.8
                else None
            ),
            order_date=datetime.now() - timedelta(
                days=random.randint(0, 365)
            ),
            status=random.choice([
                "pending",
                "preparing",
                "completed",
                "cancelled"
            ]),
            total_amount=Decimal(
                str(round(random.uniform(20, 600), 2))
            )
        )

        orders.append(order)

    # --------------------------------------
    # ORDER ITEMS: 2500
    # --------------------------------------

    order_items = []
    pares_usados = set()

    # Primero garantizamos al menos un plato por pedido
    for order in orders:
        menu_item = random.choice(menu_items)

        pares_usados.add(
            (order.order_id, menu_item.menu_item_id)
        )

        order_items.append(
            OrderItems(
                order_id=order.order_id,
                menu_item_id=menu_item.menu_item_id,
                quantity=random.randint(1, 5),
                unit_price=menu_item.price
            )
        )

    # Añadimos detalles hasta alcanzar exactamente 2500
    while len(order_items) < CANTIDADES["order_items"]:
        order = random.choice(orders)
        menu_item = random.choice(menu_items)

        pair = (order.order_id, menu_item.menu_item_id)

        if pair in pares_usados:
            continue

        pares_usados.add(pair)

        order_items.append(
            OrderItems(
                order_id=order.order_id,
                menu_item_id=menu_item.menu_item_id,
                quantity=random.randint(1, 5),
                unit_price=menu_item.price
            )
        )

    # --------------------------------------
    # PAYMENTS: 1600
    # --------------------------------------

    payments = []

    for i in range(CANTIDADES["payments"]):
        payment = Payments(
            payment_id=uuid4(),
            order_id=random.choice(orders).order_id,
            amount=Decimal(
                str(round(random.uniform(10, 600), 2))
            ),
            payment_method=random.choice([
                "cash",
                "card",
                "transfer"
            ]),
            payment_date=datetime.now() - timedelta(
                days=random.randint(0, 365)
            ),
            status=random.choice([
                "pending",
                "completed",
                "failed"
            ])
        )

        payments.append(payment)

    # --------------------------------------
    # USERS: 630
    # --------------------------------------

    users = []

    # Contraseña compartida únicamente para cuentas de demostración
    demo_password_hash = generate_password_hash("Demo1234!")

    # 600 usuarios asociados a clientes
    for i in range(600):
        user = Users(
            user_id=uuid4(),
            username=f"cliente_usuario_{i + 1}",
            password_hash=demo_password_hash,
            role="customer",
            customer_id=customers[i].customer_id,
            employee_id=None
        )

        users.append(user)

    # 27 empleados y 3 administradores
    for i in range(30):
        role = "admin" if i < 3 else "employee"

        user = Users(
            user_id=uuid4(),
            username=f"empleado_usuario_{i + 1}",
            password_hash=demo_password_hash,
            role=role,
            customer_id=None,
            employee_id=employees[i].employee_id
        )

        users.append(user)

    return {
        "customers": customers,
        "employees": employees,
        "restaurant_tables": restaurant_tables,
        "categories": categories,
        "menu_items": menu_items,
        "reservations": reservations,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "users": users
    }


# ==========================================
# INSERCIÓN EN POSTGRESQL
# ==========================================

def poblar_base_datos():
    modelos = {
        "customers": Customers,
        "employees": Employees,
        "restaurant_tables": RestaurantTables,
        "categories": Categories,
        "menu_items": MenuItems,
        "reservations": Reservations,
        "orders": Orders,
        "order_items": OrderItems,
        "payments": Payments,
        "users": Users
    }

    try:
        # Evitamos insertar otra carga si alguna tabla ya tiene datos
        for nombre, modelo in modelos.items():
            cantidad = db.session.query(modelo).count()

            if cantidad != 0:
                raise RuntimeError(
                    f"La tabla {nombre} ya tiene {cantidad} registros. "
                    "Se cancela la carga para evitar duplicados."
                )

        datos = generar_datos()

        # Orden respetando las claves foráneas
        orden_insercion = [
            "customers",
            "employees",
            "restaurant_tables",
            "categories",
            "menu_items",
            "reservations",
            "orders",
            "order_items",
            "payments",
            "users"
        ]

        for nombre in orden_insercion:
            registros = datos[nombre]

            db.session.add_all(registros)
            db.session.flush()

            print(f"{nombre}: {len(registros)} registros preparados")

        db.session.commit()

        print("\nCarga completada correctamente.")
        print("\nConteo final:")

        total = 0

        for nombre, modelo in modelos.items():
            cantidad = db.session.query(modelo).count()
            print(f"{nombre}: {cantidad}")

            total += cantidad

        print(f"\nTOTAL: {total}")

        if total != 10000:
            raise RuntimeError(
                f"Se esperaban 10000 registros, pero hay {total}."
            )

        print("Verificación correcta: hay exactamente 10000 registros.")

    except Exception as error:
        db.session.rollback()

        print(f"\nError durante la carga: {error}")
        raise
 
    finally:
        db.session.remove()


if __name__ == "__main__":
    with app.app_context():
        poblar_base_datos()