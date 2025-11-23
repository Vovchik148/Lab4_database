SELECT 
    b.book_name,
    a.name AS author,
    c.category_name
FROM books b
JOIN authors a ON b.author_id = a.author_id
JOIN books_categories bc ON b.book_id = bc.book_id
JOIN categories c ON bc.category_id = c.category_id;
