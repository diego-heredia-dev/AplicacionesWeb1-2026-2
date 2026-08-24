CREATE INDEX reservations_reservation_date_idx
ON content.reservations(reservation_date);

CREATE INDEX orders_customer_id_idx
ON content.orders(customer_id);

CREATE INDEX orders_employee_id_idx
ON content.orders(employee_id);

CREATE INDEX orders_order_date_idx
ON content.orders(order_date);