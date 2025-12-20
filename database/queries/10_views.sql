CREATE VIEW view_orders_full AS
SELECT 
    o.order_id,
    c.full_name AS customer,
    e.full_name AS employee,
    o.order_date,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id;

CREATE VIEW view_books_authors AS
SELECT 
    b.book_name,
    a.name AS author,
    b.price
FROM books b
JOIN authors a ON b.author_id = a.author_id;