EXPLAIN ANALYZE
SELECT s.company_name, b.book_name, sp.quantity, sp.delivery_date
FROM supplies sp
JOIN suppliers s ON sp.supplier_id = s.supplier_id
JOIN books b ON sp.book_id = b.book_id
WHERE sp.delivery_date > '2024-02-01';
