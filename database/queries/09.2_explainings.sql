EXPLAIN ANALYZE
SELECT 
    b.book_name,
    c.category_name
FROM books b
JOIN books_categories bc ON b.book_id = bc.book_id
JOIN categories c ON bc.category_id = c.category_id;
