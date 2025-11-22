SELECT b.book_name, a.name AS author, b.price
FROM books b
JOIN authors a ON b.author_id = a.author_id;
