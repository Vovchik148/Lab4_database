SELECT o.order_id, c.full_name AS customer, e.full_name AS employee, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id;
