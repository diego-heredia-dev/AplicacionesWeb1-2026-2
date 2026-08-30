```
Index on orders.customer_id:
Seq Scan 3.376 ms -> Bitmap Heap Scan + Bitmap Index Scan 0.225 ms

Before
"Seq Scan on orders (cost=0.00..132.50 rows=5 width=86) (actual time=0.843..3.320 rows=5 loops=1)" " Filter: (customer_id = '9b11f2b6-c864-10c9-2923-3afa11655811'::uuid)" " Rows Removed by Filter: 4995" "Planning Time: 9.884 ms" "Execution Time: 3.376 ms"

After
"Bitmap Heap Scan on orders (cost=4.32..20.37 rows=5 width=86) (actual time=0.112..0.152 rows=5 loops=1)" " Recheck Cond: (customer_id = '9b11f2b6-c864-10c9-2923-3afa11655811'::uuid)" " Heap Blocks: exact=5" " -> Bitmap Index Scan on orders_customer_id_idx (cost=0.00..4.32 rows=5 width=0) (actual time=0.079..0.079 rows=5 loops=1)" " Index Cond: (customer_id = '9b11f2b6-c864-10c9-2923-3afa11655811'::uuid)" "Planning Time: 5.829 ms" "Execution Time: 0.225 ms"
```

```
Index on orders.employee_id:
Seq Scan 3.109 ms -> Bitmap Heap Scan + Bitmap Index Scan 0.176 ms

Before
"Seq Scan on orders (cost=0.00..132.50 rows=50 width=86) (actual time=0.070..3.062 rows=50 loops=1)" " Filter: (employee_id = 'e2d93029-6ac7-7910-321b-4dec849e21c7'::uuid)" " Rows Removed by Filter: 4950" "Planning Time: 0.317 ms" "Execution Time: 3.109 ms"

After
"Bitmap Heap Scan on orders (cost=4.67..72.59 rows=50 width=86) (actual time=0.074..0.149 rows=50 loops=1)" " Recheck Cond: (employee_id = 'e2d93029-6ac7-7910-321b-4dec849e21c7'::uuid)" " Heap Blocks: exact=50" " -> Bitmap Index Scan on orders_employee_id_idx (cost=0.00..4.66 rows=50 width=0) (actual time=0.054..0.054 rows=50 loops=1)" " Index Cond: (employee_id = 'e2d93029-6ac7-7910-321b-4dec849e21c7'::uuid)" "Planning Time: 2.421 ms" "Execution Time: 0.176 ms"
```

```
Index on orders.order_date:
Seq Scan 1.952 ms -> Bitmap Heap Scan + Bitmap Index Scan 0.117 ms

Before
"Seq Scan on orders (cost=0.00..145.00 rows=8 width=86) (actual time=0.181..1.897 rows=13 loops=1)" " Filter: ((order_date >= '2026-08-20 00:00:00'::timestamp without time zone) AND (order_date < '2026-08-21 00:00:00'::timestamp without time zone))" " Rows Removed by Filter: 4987" "Planning Time: 0.704 ms" "Execution Time: 1.952 ms"

After
"Bitmap Heap Scan on orders (cost=4.36..28.37 rows=8 width=86) (actual time=0.058..0.079 rows=13 loops=1)" " Recheck Cond: ((order_date >= '2026-08-20 00:00:00'::timestamp without time zone) AND (order_date < '2026-08-21 00:00:00'::timestamp without time zone))" " Heap Blocks: exact=13" " -> Bitmap Index Scan on orders_order_date_idx (cost=0.00..4.36 rows=8 width=0) (actual time=0.023..0.023 rows=13 loops=1)" " Index Cond: ((order_date >= '2026-08-20 00:00:00'::timestamp without time zone) AND (order_date < '2026-08-21 00:00:00'::timestamp without time zone))" "Planning Time: 6.913 ms" "Execution Time: 0.117 ms"
```

```
Index on reservations.reservation_date
Seq Scan 0.491 ms -> Bitmap Index Scan + Bitmap Heap Scan 0.560 ms

Before
"Seq Scan on reservations (cost=0.00..129.50 rows=7 width=78) (actual time=0.089..0.473 rows=6 loops=1)" " Filter: (reservation_date = '2026-08-20 12:00:00'::timestamp without time zone)" " Rows Removed by Filter: 4994" "Planning Time: 1.423 ms" "Execution Time: 0.491 ms"

After
"Bitmap Heap Scan on reservations (cost=4.34..25.64 rows=7 width=78) (actual time=0.531..0.538 rows=6 loops=1)" " Recheck Cond: (reservation_date = '2026-08-20 12:00:00'::timestamp without time zone)" " Heap Blocks: exact=6" " -> Bitmap Index Scan on reservations_reservation_date_idx (cost=0.00..4.33 rows=7 width=0) (actual time=0.518..0.518 rows=6 loops=1)" " Index Cond: (reservation_date = '2026-08-20 12:00:00'::timestamp without time zone)" "Planning Time: 1.849 ms" "Execution Time: 0.560 ms"
```