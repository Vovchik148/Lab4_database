-- Книги з інформацією про авторів
CREATE OR REPLACE VIEW books_with_authors AS
SELECT
    b.book_id,
    b.book_name,
    b.isbn,
    b.publication_year,
    b.price,
    b.stock_quantity,
    a.author_id,
    a.name AS author_name,
    a.country AS author_country,
    a.birth_year AS author_birth_year
FROM books b
INNER JOIN authors a ON b.author_id = a.author_id;


-- Статистика по авторах
CREATE OR REPLACE VIEW author_statistics AS
SELECT
    a.author_id,
    a.name AS author_name,
    a.country,
    COUNT(b.book_id) AS total_books,
    AVG(b.price)::DECIMAL(10,2) AS avg_book_price,
    SUM(b.stock_quantity) AS total_stock,
    MIN(b.publication_year) AS first_publication,
    MAX(b.publication_year) AS last_publication
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name, a.country;


-- Найдорожча книга кожного автора
CREATE OR REPLACE VIEW expensive_books_by_author AS
SELECT DISTINCT ON (a.author_id)
    a.author_id,
    a.name AS author_name,
    b.book_name AS most_expensive_book,
    b.price AS highest_price
FROM authors a
INNER JOIN books b ON a.author_id = b.author_id
ORDER BY a.author_id, b.price DESC;