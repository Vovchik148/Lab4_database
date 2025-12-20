EXPLAIN ANALYZE
SELECT 
    o.order_id,
    c.full_name,
    e.full_name,
    b.book_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN books b ON oi.book_id = b.book_id;
