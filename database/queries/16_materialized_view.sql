CREATE MATERIALIZED VIEW mv_sales_summary AS
SELECT 
    b.book_name,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN books b ON oi.book_id = b.book_id
GROUP BY b.book_name;


CREATE OR REPLACE FUNCTION refresh_mv_books_sales()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_books_sales;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_refresh_mv_books_sales_ins
AFTER INSERT ON order_items
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_mv_books_sales();

CREATE TRIGGER trg_refresh_mv_books_sales_upd
AFTER UPDATE ON order_items
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_mv_books_sales();

CREATE TRIGGER trg_refresh_mv_books_sales_del
AFTER DELETE ON order_items
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_mv_books_sales();