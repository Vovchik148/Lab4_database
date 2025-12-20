CREATE INDEX idx_books_expensive ON books(price)
WHERE price > 400;

CREATE INDEX idx_orders_recent ON orders(order_date)
WHERE order_date > '2024-03-01';
