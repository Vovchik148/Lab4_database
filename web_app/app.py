from flask import Flask, render_template, request, redirect, url_for, flash
from db import DatabaseConnection
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

db = DatabaseConnection(
    dbname='bookstore',
    user='postgres',
    password='password',
    host='localhost',
    port=5432
)
db.connect()


# ------------------------------------------------
# ГОЛОВНІ СТОРІНКИ
# ------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    counts = {}

    for name, table in [
        ('books', 'books'),
        ('authors', 'authors'),
        ('categories', 'categories')
    ]:
        cursor = db.execute_query(f"SELECT COUNT(*) FROM {table}")
        counts[name] = cursor.fetchone()[0] if cursor else 0

    return render_template('dashboard.html', counts=counts)


# ------------------------------------------------
# КНИГИ
# ------------------------------------------------
@app.route('/books')
def books():
    query = """
        SELECT 
            b.book_id,
            b.book_name,
            b.isbn,
            b.publication_year,
            b.price,
            b.stock_quantity,
            a.name AS author_name,
            COALESCE(string_agg(c.category_name, ', ' ORDER BY c.category_name), '') AS categories
        FROM books b
        INNER JOIN authors a ON b.author_id = a.author_id
        LEFT JOIN books_categories bc ON b.book_id = bc.book_id
        LEFT JOIN categories c ON bc.category_id = c.category_id
        GROUP BY b.book_id, b.book_name, b.isbn, b.publication_year, b.price, b.stock_quantity, a.name
        ORDER BY b.book_name;
    """
    cursor = db.execute_query(query)
    books_list = cursor.fetchall() if cursor else []
    return render_template('books.html', books=books_list)


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        isbn = request.form['isbn']
        year = int(request.form['year'])
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        author_id = int(request.form['author_id'])
        category_ids = request.form.getlist('categories')

        insert_book = """
            INSERT INTO books (book_name, isbn, publication_year, price, stock_quantity, author_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING book_id;
        """
        cursor = db.execute_query(insert_book, (book_name, isbn, year, price, stock, author_id))

        if not cursor:
            flash('Помилка додавання книги', 'error')
            return redirect(url_for('books'))

        book_id = cursor.fetchone()[0]

        if category_ids:
            insert_bc = """
                INSERT INTO books_categories (book_id, category_id)
                VALUES (%s, %s)
            """
            for cid in category_ids:
                db.execute_query(insert_bc, (book_id, int(cid)))

        flash('Книгу успішно додано!', 'success')
        return redirect(url_for('books'))

    authors_q = "SELECT author_id, name FROM authors ORDER BY name"
    cursor_a = db.execute_query(authors_q)
    authors = cursor_a.fetchall() if cursor_a else []

    categories_q = "SELECT category_id, category_name FROM categories ORDER BY category_name"
    cursor_c = db.execute_query(categories_q)
    categories = cursor_c.fetchall() if cursor_c else []

    return render_template('add_book.html', authors=authors, categories=categories)


@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if request.method == 'POST':
        book_name = request.form['book_name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        author_id = int(request.form['author_id'])
        category_ids = request.form.getlist('categories')

        update_book = """
            UPDATE books
            SET book_name = %s,
                price = %s,
                stock_quantity = %s,
                author_id = %s
            WHERE book_id = %s;
        """
        cursor = db.execute_query(update_book, (book_name, price, stock, author_id, book_id))

        if not cursor:
            flash('Помилка оновлення книги', 'error')
            return redirect(url_for('books'))

        db.execute_query("DELETE FROM books_categories WHERE book_id = %s", (book_id,))
        insert_bc = "INSERT INTO books_categories (book_id, category_id) VALUES (%s, %s)"
        for cid in category_ids:
            db.execute_query(insert_bc, (book_id, int(cid)))

        flash('Книгу успішно оновлено!', 'success')
        return redirect(url_for('books'))

    book_q = """
        SELECT 
            b.book_id,
            b.book_name,
            b.isbn,
            b.publication_year,
            b.price,
            b.stock_quantity,
            a.author_id,
            a.name AS author_name
        FROM books b
        INNER JOIN authors a ON b.author_id = a.author_id
        WHERE b.book_id = %s;
    """
    cursor_b = db.execute_query(book_q, (book_id,))
    book = cursor_b.fetchone() if cursor_b else None

    if not book:
        flash('Книгу не знайдено', 'error')
        return redirect(url_for('books'))

    current_cq = "SELECT category_id FROM books_categories WHERE book_id = %s"
    cursor_cc = db.execute_query(current_cq, (book_id,))
    current_categories = {row[0] for row in cursor_cc.fetchall()} if cursor_cc else set()

    authors_q = "SELECT author_id, name FROM authors ORDER BY name"
    cursor_a = db.execute_query(authors_q)
    authors = cursor_a.fetchall() if cursor_a else []

    categories_q = "SELECT category_id, category_name FROM categories ORDER BY category_name"
    cursor_c = db.execute_query(categories_q)
    categories = cursor_c.fetchall() if cursor_c else []

    return render_template(
        'edit_book.html',
        book=book,
        authors=authors,
        categories=categories,
        current_categories=current_categories
    )


@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    db.execute_query("DELETE FROM books_categories WHERE book_id = %s", (book_id,))
    cursor = db.execute_query("DELETE FROM books WHERE book_id = %s", (book_id,))

    if cursor:
        flash('Книгу успішно видалено!', 'success')
    else:
        flash('Помилка видалення книги', 'error')

    return redirect(url_for('books'))


# ------------------------------------------------
# АВТОРИ
# ------------------------------------------------
@app.route('/authors')
def authors():
    query = "SELECT author_id, name, birth_year, country FROM authors ORDER BY name"
    cursor = db.execute_query(query)
    authors_list = cursor.fetchall() if cursor else []
    return render_template('authors.html', authors=authors_list)


@app.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_year = int(request.form['birth_year']) if request.form['birth_year'] else None
        country = request.form['country']

        query = "INSERT INTO authors (name, birth_year, country) VALUES (%s, %s, %s)"
        cursor = db.execute_query(query, (name, birth_year, country))

        if cursor:
            flash('Автора успішно додано!', 'success')
            return redirect(url_for('authors'))
        else:
            flash('Помилка додавання автора', 'error')

    return render_template('add_author.html')


@app.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    if request.method == 'POST':
        name = request.form['name']
        birth_year = int(request.form['birth_year']) if request.form['birth_year'] else None
        country = request.form['country']

        query = """
            UPDATE authors
            SET name = %s, birth_year = %s, country = %s
            WHERE author_id = %s
        """
        cursor = db.execute_query(query, (name, birth_year, country, author_id))

        if cursor:
            flash('Дані автора оновлено!', 'success')
            return redirect(url_for('authors'))
        else:
            flash('Помилка оновлення автора', 'error')

    query = "SELECT author_id, name, birth_year, country FROM authors WHERE author_id = %s"
    cursor = db.execute_query(query, (author_id,))
    author = cursor.fetchone() if cursor else None

    if not author:
        flash('Автора не знайдено', 'error')
        return redirect(url_for('authors'))

    return render_template('edit_author.html', author=author)


@app.route('/authors/delete/<int:author_id>')
def delete_author(author_id):
    cursor = db.execute_query("DELETE FROM authors WHERE author_id = %s", (author_id,))

    if cursor:
        flash('Автора видалено (або вдалось видалити без помилок)', 'success')
    else:
        flash('Не вдалося видалити автора (можливо, є пов’язані книги)', 'error')

    return redirect(url_for('authors'))


# ------------------------------------------------
# КАТЕГОРІЇ
# ------------------------------------------------
@app.route('/categories')
def categories():
    query = "SELECT category_id, category_name FROM categories ORDER BY category_name"
    cursor = db.execute_query(query)
    categories_list = cursor.fetchall() if cursor else []
    return render_template('categories.html', categories=categories_list)


@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['category_name']
        query = "INSERT INTO categories (category_name) VALUES (%s)"
        cursor = db.execute_query(query, (name,))

        if cursor:
            flash('Категорію додано!', 'success')
            return redirect(url_for('categories'))
        else:
            flash('Помилка додавання категорії', 'error')

    return render_template('add_category.html')


@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        name = request.form['category_name']
        query = "UPDATE categories SET category_name = %s WHERE category_id = %s"
        cursor = db.execute_query(query, (name, category_id))

        if cursor:
            flash('Категорію оновлено!', 'success')
            return redirect(url_for('categories'))
        else:
            flash('Помилка оновлення категорії', 'error')

    query = "SELECT category_id, category_name FROM categories WHERE category_id = %s"
    cursor = db.execute_query(query, (category_id,))
    category = cursor.fetchone() if cursor else None

    if not category:
        flash('Категорію не знайдено', 'error')
        return redirect(url_for('categories'))

    return render_template('edit_category.html', category=category)


@app.route('/categories/delete/<int:category_id>')
def delete_category(category_id):
    db.execute_query("DELETE FROM books_categories WHERE category_id = %s", (category_id,))
    cursor = db.execute_query("DELETE FROM categories WHERE category_id = %s", (category_id,))

    if cursor:
        flash('Категорію видалено!', 'success')
    else:
        flash('Не вдалося видалити категорію', 'error')

    return redirect(url_for('categories'))


# ------------------------------------------------
# СТАТИСТИКА АВТОРІВ (VIEW author_statistics)
# ------------------------------------------------
@app.route('/author_statistics')
def author_statistics():
    query = "SELECT * FROM author_statistics ORDER BY total_books DESC"
    cursor = db.execute_query(query)
    stats = cursor.fetchall() if cursor else []

    return render_template('author_statistics.html', stats=stats)


# ------------------------------------------------
# Запуск
# ------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)