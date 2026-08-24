BEGIN;

-- ============================================
-- CUSTOMERS: 1,000
-- ============================================

INSERT INTO content.customers (
    customer_id,
    first_name,
    last_name,
    email,
    phone
)
SELECT
    md5('customer-' || gs)::uuid,
    'Customer' || gs,
    'Lastname' || gs,
    'customer' || gs || '@example.com',
    '700000' || LPAD(gs::text, 4, '0')
FROM generate_series(1, 1000) AS gs;


-- ============================================
-- EMPLOYEES: 100
-- ============================================

INSERT INTO content.employees (
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    role,
    hire_date
)
SELECT
    md5('employee-' || gs)::uuid,
    'Employee' || gs,
    'Lastname' || gs,
    'employee' || gs || '@restaurant.com',
    '600000' || LPAD(gs::text, 4, '0'),
    CASE
        WHEN gs % 4 = 0 THEN 'Manager'
        WHEN gs % 4 = 1 THEN 'Waiter'
        WHEN gs % 4 = 2 THEN 'Chef'
        ELSE 'Cashier'
    END,
    DATE '2020-01-01' + (gs % 2000)
FROM generate_series(1, 100) AS gs;


-- ============================================
-- RESTAURANT TABLES: 50
-- ============================================

INSERT INTO content.restaurant_tables (
    table_id,
    table_number,
    capacity,
    available
)
SELECT
    md5('table-' || gs)::uuid,
    gs,
    CASE
        WHEN gs % 4 = 0 THEN 2
        WHEN gs % 4 = 1 THEN 4
        WHEN gs % 4 = 2 THEN 6
        ELSE 8
    END,
    CASE
        WHEN gs % 5 = 0 THEN FALSE
        ELSE TRUE
    END
FROM generate_series(1, 50) AS gs;


-- ============================================
-- MENU ITEMS: 100
-- ============================================

INSERT INTO content.menu_items (
    menu_item_id,
    name,
    description,
    price,
    available
)
SELECT
    md5('menu-item-' || gs)::uuid,
    'Menu Item ' || gs,
    'Description for menu item ' || gs,
    ROUND((5 + (gs % 50) * 1.25)::numeric, 2),
    CASE
        WHEN gs % 10 = 0 THEN FALSE
        ELSE TRUE
    END
FROM generate_series(1, 100) AS gs;


-- ============================================
-- RESERVATIONS: 5,000
-- ============================================

INSERT INTO content.reservations (
    reservation_id,
    customer_id,
    table_id,
    reservation_date,
    party_size,
    status,
    created_at
)
SELECT
    md5('reservation-' || gs)::uuid,
    md5('customer-' || (((gs - 1) % 1000) + 1))::uuid,
    md5('table-' || (((gs - 1) % 50) + 1))::uuid,
    TIMESTAMP '2026-08-20 12:00:00'
        + ((gs % 365) * INTERVAL '1 day')
        + ((gs % 10) * INTERVAL '1 hour'),
    ((gs - 1) % 6) + 1,
    CASE
        WHEN gs % 10 = 0 THEN 'Cancelled'
        WHEN gs % 5 = 0 THEN 'Completed'
        ELSE 'Confirmed'
    END,
    TIMESTAMP '2026-01-01 08:00:00'
        + ((gs % 200) * INTERVAL '1 day')
FROM generate_series(1, 5000) AS gs;


-- ============================================
-- ORDERS: 5,000
-- ============================================

INSERT INTO content.orders (
    order_id,
    customer_id,
    employee_id,
    table_id,
    order_date,
    status,
    total_amount
)
SELECT
    md5('order-' || gs)::uuid,

    -- Every 10th order has no registered customer
    CASE
        WHEN gs % 10 = 0 THEN NULL
        ELSE md5('customer-' || (((gs - 1) % 1000) + 1))::uuid
    END,

    md5('employee-' || (((gs - 1) % 100) + 1))::uuid,

    -- Every 5th order is takeout
    CASE
        WHEN gs % 5 = 0 THEN NULL
        ELSE md5('table-' || (((gs - 1) % 50) + 1))::uuid
    END,

    TIMESTAMP '2026-08-20 10:00:00'
        + ((gs % 365) * INTERVAL '1 day')
        + ((gs % 12) * INTERVAL '1 hour'),

    CASE
        WHEN gs % 10 = 0 THEN 'Cancelled'
        WHEN gs % 5 = 0 THEN 'Completed'
        ELSE 'Pending'
    END,

    ROUND((10 + (gs % 200) * 1.50)::numeric, 2)

FROM generate_series(1, 5000) AS gs;


-- ============================================
-- ORDER ITEMS: 15,000
-- 3 items per order
-- ============================================

INSERT INTO content.order_items (
    order_id,
    menu_item_id,
    quantity,
    unit_price
)
SELECT
    md5('order-' || order_number)::uuid,
    md5('menu-item-' || menu_number)::uuid,
    ((order_number + item_number) % 4) + 1,
    ROUND((5 + (menu_number % 50) * 1.25)::numeric, 2)

FROM generate_series(1, 5000) AS order_number
CROSS JOIN generate_series(1, 3) AS item_number

CROSS JOIN LATERAL (
    SELECT
        ((order_number + item_number - 1) % 100) + 1 AS menu_number
) AS menu;


-- ============================================
-- PAYMENTS: 5,000
-- ============================================

INSERT INTO content.payments (
    payment_id,
    order_id,
    amount,
    payment_method,
    payment_date,
    status
)
SELECT
    md5('payment-' || gs)::uuid,
    md5('order-' || gs)::uuid,
    ROUND((10 + (gs % 200) * 1.50)::numeric, 2),
    CASE
        WHEN gs % 4 = 0 THEN 'Cash'
        WHEN gs % 4 = 1 THEN 'Card'
        WHEN gs % 4 = 2 THEN 'Transfer'
        ELSE 'Mobile'
    END,
    TIMESTAMP '2026-08-20 10:30:00'
        + ((gs % 365) * INTERVAL '1 day')
        + ((gs % 12) * INTERVAL '1 hour'),
    CASE
        WHEN gs % 10 = 0 THEN 'Refunded'
        ELSE 'Completed'
    END
FROM generate_series(1, 5000) AS gs;


COMMIT;