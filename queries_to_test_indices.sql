EXPLAIN ANALYZE
SELECT *
FROM content.reservations
WHERE reservation_date = '2026-08-20 12:00:00';

EXPLAIN ANALYZE
SELECT *
FROM content.orders
WHERE customer_id = '9b11f2b6-c864-10c9-2923-3afa11655811';

EXPLAIN ANALYZE
SELECT *
FROM content.orders
WHERE employee_id = 'e2d93029-6ac7-7910-321b-4dec849e21c7';

EXPLAIN ANALYZE
SELECT *
FROM content.orders
WHERE order_date >= '2026-08-20 00:00:00'
  AND order_date < '2026-08-21 00:00:00';
