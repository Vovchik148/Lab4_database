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
    isbn varchar(30) unique,
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
