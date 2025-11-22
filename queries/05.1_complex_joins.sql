SELECT 
    oi.order_item_id,
    b.book_name,
    c.full_name AS customer,
    e.full_name AS employee,
    oi.quantity,
    oi.unit_price
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id
JOIN books b ON oi.book_id = b.book_id;
