CREATE VIEW view_books_prices AS
SELECT book_id, book_name, price FROM books;

CREATE RULE update_price AS
ON UPDATE TO view_books_prices
DO INSTEAD
UPDATE books SET price = NEW.price WHERE book_id = OLD.book_id;