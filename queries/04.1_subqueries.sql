SELECT book_name, price
FROM books
WHERE price > (SELECT AVG(price) FROM books);
