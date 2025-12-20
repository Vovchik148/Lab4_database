CREATE OR REPLACE FUNCTION validate_book_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price <= 0 THEN
        RAISE EXCEPTION 'Ціна не може бути нуль або відʼємна';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_price
BEFORE INSERT ON books
FOR EACH ROW
EXECUTE FUNCTION validate_book_price();