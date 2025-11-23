-- Логування змін цін книг у таблиці books
CREATE OR REPLACE FUNCTION log_book_price_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND OLD.price != NEW.price THEN
        INSERT INTO book_audit (book_id, operation, old_price, new_price, changed_by)
        VALUES (NEW.book_id, 'UPDATE', OLD.price, NEW.price, current_user);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER book_price_audit
AFTER UPDATE ON books
FOR EACH ROW
EXECUTE FUNCTION log_book_price_change();


-- Автоматичне оновлення timestamp при зміні запису в таблиці authors
CREATE OR REPLACE FUNCTION update_book_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER book_update_timestamp
BEFORE UPDATE ON books
FOR EACH ROW
EXECUTE FUNCTION update_book_timestamp();


-- Валідація даних книги перед вставкою або оновленням
CREATE OR REPLACE FUNCTION validate_book_data()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.publication_year > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'Рік видання не може бути у майбутньому';
    END IF;

    IF NEW.price < 0 THEN
        RAISE EXCEPTION 'Ціна не може бути від''ємною';
    END IF;

    IF NEW.stock_quantity < 0 THEN
        RAISE EXCEPTION 'Кількість на складі не може бути від''ємною';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_book_before_write
BEFORE INSERT OR UPDATE ON books
FOR EACH ROW
EXECUTE FUNCTION validate_book_data();