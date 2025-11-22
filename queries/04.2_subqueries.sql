SELECT order_id, total_amount
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders);
