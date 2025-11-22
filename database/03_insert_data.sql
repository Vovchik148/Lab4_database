-- authors
INSERT INTO authors (name, birth_year, country) VALUES
('Джоан Роулінг', 1965, 'Велика Британія'),
('Джордж Мартін', 1948, 'США'),
('Стівен Кінг', 1947, 'США'),
('Френк Герберт', 1920, 'США'),
('Олдос Гакслі', 1894, 'Велика Британія');

-- categories
INSERT INTO categories (category_name) VALUES
('Фентезі'),
('Пригоди'),
('Жахи'),
('Наукова фантастика'),
('Антиутопія');

-- books
INSERT INTO books (isbn, book_name, author_id, publication_year, price, stock_quantity) VALUES
('9781408855652', 'Гаррі Поттер і філософський камінь', 1, 1997, 380, 25),
('9780553103540', 'Гра Престолів', 2, 1996, 450, 18),
('9780307743657', 'Сяйво', 3, 1977, 320, 12),
('9780441172719', 'Дюна', 4, 1965, 410, 20),
('9780060850524', 'О дивний новий світ', 5, 1932, 300, 10);

-- books_categories
INSERT INTO books_categories (book_id, category_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 3),
(4, 4),
(5, 5);

-- suppliers
INSERT INTO suppliers (company_name, phone, email) VALUES
('BookLine', '+380931112233', 'bookline@gmail.com'),
('ReadersHub', '+380671234567', 'readershub@gmail.com'),
('WorldBooks', '+380501111222', 'worldbooks@gmail.com');

-- supplies
INSERT INTO supplies (supplier_id, book_id, quantity, delivery_date) VALUES
(1, 1, 40, '2024-01-12'),
(1, 3, 25, '2024-02-15'),
(2, 2, 30, '2024-01-29'),
(2, 4, 20, '2024-03-01'),
(3, 5, 15, '2024-02-20');

-- customers
INSERT INTO customers (full_name, phone, email) VALUES
('Іван Петренко', '+380991112233', 'ivan.petrenko@gmail.com'),
('Марія Коваленко', '+380931234567', 'maria.k@gmail.com'),
('Олександр Шевченко', '+380501234111', 'oleksandr.sh@gmail.com');

-- employees
INSERT INTO employees (full_name, position, salary) VALUES
('Анна Степаненко', 'Продавець', 15000),
('Олег Бондар', 'Менеджер', 21000),
('Світлана Романюк', 'Адміністратор', 25000);

-- orders
INSERT INTO orders (customer_id, employee_id, order_date, total_amount) VALUES
(1, 1, '2024-03-10', 760),
(2, 1, '2024-03-12', 410),
(3, 2, '2024-03-14', 380);

-- order_items
INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES
(1, 1, 1, 380),
(1, 3, 1, 320),
(2, 4, 1, 410),
(3, 1, 1, 380);
