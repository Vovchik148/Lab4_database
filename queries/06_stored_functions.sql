-- Додавання книги з автоматичним створенням автора, якщо він не існує
CREATE OR REPLACE FUNCTION add_book_with_author(
    p_book_name VARCHAR,
    p_isbn VARCHAR,
    p_publication_year INT,
    p_price DECIMAL,
    p_stock INT,
    p_author_name VARCHAR,
    p_birth_year INT,
    p_country VARCHAR
) RETURNS INT AS $$
DECLARE
    v_author_id INT;
    v_book_id INT;
BEGIN
    SELECT author_id INTO v_author_id
    FROM authors
    WHERE name = p_author_name;

    IF v_author_id IS NULL THEN
        INSERT INTO authors (name, birth_year, country)
        VALUES (p_author_name, p_birth_year, p_country)
        RETURNING author_id INTO v_author_id;
    END IF;

    INSERT INTO books (book_name, isbn, publication_year, price, stock_quantity, author_id)
    VALUES (p_book_name, p_isbn, p_publication_year, p_price, p_stock, v_author_id)
    RETURNING book_id INTO v_book_id;

    RETURN v_book_id;
END;
$$ LANGUAGE plpgsql;


-- Оновлення цін на книги автора з відсотковою знижкою
CREATE OR REPLACE FUNCTION update_author_books_price(
    p_author_id INT,
    p_discount_percent DECIMAL
) RETURNS TABLE(book_id INT, old_price DECIMAL, new_price DECIMAL) AS $$
BEGIN
    RETURN QUERY
    UPDATE books
    SET price = price * (1 - p_discount_percent / 100)
    WHERE author_id = p_author_id
    RETURNING 
        book_id,
        price / (1 - p_discount_percent / 100) AS old_price,
        price AS new_price;
END;
$$ LANGUAGE plpgsql;


-- Отримання статистики по книгах автора
CREATE OR REPLACE FUNCTION get_author_statistics(p_author_id INT)
RETURNS TABLE(
    total_books INT,
    avg_price DECIMAL,
    min_price DECIMAL,
    max_price DECIMAL,
    total_stock INT,
    earliest_year INT,
    latest_year INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*)::INT AS total_books,
        AVG(price)::DECIMAL(10,2) AS avg_price,
        MIN(price)::DECIMAL(10,2) AS min_price,
        MAX(price)::DECIMAL(10,2) AS max_price,
        SUM(stock_quantity)::INT AS total_stock,
        MIN(publication_year)::INT AS earliest_year,
        MAX(publication_year)::INT AS latest_year
    FROM books
    WHERE author_id = p_author_id;
END;
$$ LANGUAGE plpgsql;
