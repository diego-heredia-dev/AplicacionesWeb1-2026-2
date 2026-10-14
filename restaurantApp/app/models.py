from .extensions import db


# ==========================================
# CUSTOMERS
# ==========================================

class Customers(db.Model):
    __tablename__ = "customers"
    __table_args__ = {"schema": "content"}

    customer_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(30), unique=True)

    # Soft delete
    is_deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.text("false")
    )

    # Relationships
    reservations = db.relationship(
        "Reservations",
        back_populates="customer"
    )

    orders = db.relationship(
        "Orders",
        back_populates="customer"
    )

    user = db.relationship(
        "Users",
        back_populates="customer",
        uselist=False
    )


# ==========================================
# EMPLOYEES
# ==========================================

class Employees(db.Model):
    __tablename__ = "employees"
    __table_args__ = {"schema": "content"}

    employee_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=False, unique=True)

    # Work position, for example: waiter, cook or manager
    role = db.Column(db.String(50), nullable=False)

    hire_date = db.Column(db.Date, nullable=False)

    # Soft delete
    is_deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.text("false")
    )

    # Relationships
    orders = db.relationship(
        "Orders",
        back_populates="employee"
    )

    user = db.relationship(
        "Users",
        back_populates="employee",
        uselist=False
    )


# ==========================================
# RESTAURANT TABLES
# ==========================================

class RestaurantTables(db.Model):
    __tablename__ = "restaurant_tables"
    __table_args__ = (
        db.CheckConstraint(
            "capacity > 0",
            name="ck_table_capacity"
        ),
        {"schema": "content"}
    )

    table_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    table_number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    available = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default=db.text("true")
    )

    # Soft delete
    is_deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.text("false")
    )

    # Relationships
    reservations = db.relationship(
        "Reservations",
        back_populates="table"
    )

    orders = db.relationship(
        "Orders",
        back_populates="table"
    )


# ==========================================
# CATEGORIES
# ==========================================

class Categories(db.Model):
    __tablename__ = "categories"
    __table_args__ = {"schema": "content"}

    category_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    # Relationships
    menu_items = db.relationship(
        "MenuItems",
        back_populates="category"
    )


# ==========================================
# MENU ITEMS
# ==========================================

class MenuItems(db.Model):
    __tablename__ = "menu_items"
    __table_args__ = (
        db.CheckConstraint(
            "price > 0",
            name="ck_menu_item_price"
        ),
        {"schema": "content"}
    )

    menu_item_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    category_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.categories.category_id"),
        nullable=False
    )

    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    available = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default=db.text("true")
    )

    # Relationships
    category = db.relationship(
        "Categories",
        back_populates="menu_items"
    )

    order_items = db.relationship(
        "OrderItems",
        back_populates="menu_item"
    )


# ==========================================
# RESERVATIONS
# ==========================================

class Reservations(db.Model):
    __tablename__ = "reservations"
    __table_args__ = (
        db.CheckConstraint(
            "party_size > 0",
            name="ck_reservation_party_size"
        ),
        {"schema": "content"}
    )

    reservation_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    customer_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.customers.customer_id"),
        nullable=False
    )

    table_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.restaurant_tables.table_id"),
        nullable=False
    )

    reservation_date = db.Column(db.DateTime, nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    # Relationships
    customer = db.relationship(
        "Customers",
        back_populates="reservations"
    )

    table = db.relationship(
        "RestaurantTables",
        back_populates="reservations"
    )


# ==========================================
# ORDERS
# ==========================================

class Orders(db.Model):
    __tablename__ = "orders"
    __table_args__ = (
        db.CheckConstraint(
            "total_amount > 0",
            name="ck_order_total_amount"
        ),
        {"schema": "content"}
    )

    order_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    customer_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.customers.customer_id"),
        nullable=True
    )

    employee_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.employees.employee_id"),
        nullable=False
    )

    table_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.restaurant_tables.table_id"),
        nullable=True
    )

    order_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    status = db.Column(db.String(30), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    customer = db.relationship(
        "Customers",
        back_populates="orders"
    )

    employee = db.relationship(
        "Employees",
        back_populates="orders"
    )

    table = db.relationship(
        "RestaurantTables",
        back_populates="orders"
    )

    order_items = db.relationship(
        "OrderItems",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    payments = db.relationship(
        "Payments",
        back_populates="order"
    )


# ==========================================
# ORDER ITEMS
# ==========================================

class OrderItems(db.Model):
    __tablename__ = "order_items"
    __table_args__ = (
        db.CheckConstraint(
            "quantity > 0",
            name="ck_order_item_quantity"
        ),
        db.CheckConstraint(
            "unit_price > 0",
            name="ck_order_item_unit_price"
        ),
        {"schema": "content"}
    )

    order_id = db.Column(
        db.Uuid,
        db.ForeignKey(
            "content.orders.order_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    menu_item_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.menu_items.menu_item_id"),
        primary_key=True
    )

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
    order = db.relationship(
        "Orders",
        back_populates="order_items"
    )

    menu_item = db.relationship(
        "MenuItems",
        back_populates="order_items"
    )


# ==========================================
# PAYMENTS
# ==========================================

class Payments(db.Model):
    __tablename__ = "payments"
    __table_args__ = (
        db.CheckConstraint(
            "amount > 0",
            name="ck_payment_amount"
        ),
        {"schema": "content"}
    )

    payment_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    order_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.orders.order_id"),
        nullable=False
    )

    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)

    payment_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    status = db.Column(db.String(30), nullable=False)

    # Relationships
    order = db.relationship(
        "Orders",
        back_populates="payments"
    )


# ==========================================
# USERS
# ==========================================

class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.CheckConstraint(
            "role IN ('customer', 'employee', 'admin')",
            name="ck_users_role"
        ),
        db.CheckConstraint(
            """
            (
                role = 'customer'
                AND customer_id IS NOT NULL
                AND employee_id IS NULL
            )
            OR
            (
                role IN ('employee', 'admin')
                AND customer_id IS NULL
                AND employee_id IS NOT NULL
            )
            """,
            name="ck_users_owner"
        ),
        {"schema": "content"}
    )

    user_id = db.Column(
        db.Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()")
    )

    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    customer_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.customers.customer_id"),
        unique=True
    )

    employee_id = db.Column(
        db.Uuid,
        db.ForeignKey("content.employees.employee_id"),
        unique=True
    )

    # Relationships
    customer = db.relationship(
        "Customers",
        back_populates="user"
    )

    employee = db.relationship(
        "Employees",
        back_populates="user"
    )