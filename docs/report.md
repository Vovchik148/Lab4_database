# Звіт з лабораторної роботи №4

## Загальна інформація
- ПІБ студента: Шипкін Денис.
- Група: ІПЗ-32.
- Варіант Система обліку книжкового магазину.
- Рівень виконання: 3.

## Опис предметної області
Книжковий магазин — це таке собі "підприємство", основною діяльністю якого є продаж книг. Магазин працює з різними видами товарів, постачальниками та категоріями читачів, тому потребує чіткого ведення обліку, контролю запасів та управління процесами продажу.
У межах предметної області відбувається рух товарів від постачальників до складу магазину та далі до покупця, що супроводжується документальним оформленням, реєстрацією операцій та контролем даних.

## Концептуальна модель
### Книги:
- ISBN
- Назва
- Автор
- Видавництво
- Рік видання
- Жанр / категорія
- Ціна закупівельна
- Ціна продажу
- Кількість на складі
- Мова

### Автори:
- ПІБ
- Рік народження
- Країна

### Постачальники:
- Назва компанії
- Контакти
- Сума

### Покупці
- ПІБ
- Телефон
- Email

### Продажі
- Дата продажу
- Товар
- Кількість
- Сума
- Продавець(співробітник магазину)

### Працівники
- ПІБ
- Посада (продавець, менеджер, адміністратор)
- Ставка/зарплата (якщо потрібно)

### Зв'язки:
Автор 1 — N Книги
Книга M — N Постачальник (через Supplies)
Книга M — N Продаж (через Sale_Items)
Покупець 1 — N Продаж
Працівник 1 — N Продаж
Категорія 1 — N Книга
Книга 1 — N Поставки

До уваги: це приблизні зв'язки, не факт що вони будуть такі самі наприкінці!!!

[ER-діаграма](/docs/conceptual_model.png)

## Логічна схема
authors
--------
author_id       PK
full_name
birth_year
country

categories
------------
category_id     PK
name

books
--------
book_id         PK
isbn
title
author_id       FK → Authors.author_id
category_id     FK → Categories.category_id
publication_year
purchase_price
sale_price
stock_quantity

suppliers
-----------
supplier_id     PK
company_name
contacts

supplies
---------
supply_id       PK
supplier_id     FK → Suppliers.supplier_id
book_id         FK → Books.book_id
quantity
purchase_price
delivery_date

customers
-----------
customer_id     PK
full_name
phone
email

employees
-----------
employee_id     PK
full_name
position
salary

sales
--------
sale_id         PK
sale_date
customer_id     FK → Customers.customer_id
employee_id     FK → Employees.employee_id
total_amount

sale_Items       -- позиції чека (зв’язок M:N: продаж-книга)
-----------
sale_id         FK → Sales.sale_id
book_id         FK → Books.book_id
quantity
price_at_sale

## Реалізація в PostgreSQL
```sql
create table authors (
    author_id serial primary key,
    name varchar(50),
    birth_year int,
    country varchar(30)
);

create table categories (
    category_id serial primary key,
    category_name varchar(20)
);

create table books (
    book_id serial primary key,
    isbn integer unique,
    book_name varchar(50),
    author_id int references authors(author_id),
    publication_year int,
    price decimal,
    stock_quantity int
);

create table books_categories (
    book_id integer references books(book_id),
    category_id integer references categories(category_id),
    primary key (book_id, category_id)
);

create table suppliers (
  supplier_id serial primary key,
  company_name varchar(40),
  phone varchar unique,
  email varchar unique
);

create table supplies (
    supply_id serial primary key,
    supplier_id integer references suppliers(supplier_id),
    book_id integer references books(book_id),
    quantity integer,
    delivery_date date
);

create table customers (
    customer_id serial primary key,
    full_name varchar(50),
    phone varchar(20) unique,
    email varchar(50) unique
);

create table employees (
    employee_id serial primary key,
    full_name varchar(50),
    position varchar(30),
    salary decimal
);

create table orders (
    order_id serial primary key,
    customer_id integer references customers(customer_id),
    employee_id integer references employees(employee_id),
    order_date date,
    total_amount decimal
);

create table order_items (
    order_item_id serial primary key,
    order_id integer references orders(order_id),
    book_id integer references books(book_id),
    quantity integer,
    unit_price decimal
);
```

## Налаштування Docker
docker-compose.yml містить у собі інформацію, яка допомагає Docker-у працювати з нашою БД, а саме він містить інформацію про те, яку версію СУБД ми використовуємо, її ім'я, дані входу, порти, створення томів даних для збереження, наприклад, результатів виконання sql-запитів. Також цей файл містить у собі інформацію про створення сторінки pgAdmin, а саме її ім'я, дані входу і порт. 

### Для роботи із контейнером Docker, який уже під'єнаний до проєкту, неохідно знати декілька команд:
- docker-compose up -d -- запуск БД у фоновому режимі;
- docker-compose ps -- перевірка статусу контейнера;
- docker exec -it bookstore_db psql -U postgres -d bookstore -- відкриття термінал psql (за умови, що psql підключено до проєкту);
- docker-compose stop -- зупинка контейнеру;
- docker-compose start -- запуск контейнеру;
- docker-compose down -v -- повне очищення контейнеру разом із volumes;
- docker-compose up -d --force-recreate -- перезавантаження контейнеру з оновленою інформацією. 

## SQL-запити
[Приклади запитів з поясненням]

## Вебзастосунок
[Відео](/docs/Web_application.mp4)


## Розширена функціональність (рівень 3, якщо реалізовано)
[Опис реалізованих додаткових можливостей]

## Висновки
[Що було зроблено, які навички здобуто, які труднощі виникли]