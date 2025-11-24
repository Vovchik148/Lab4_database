from flask import jsonify, request
from functools import wraps

# ======================================================
#   API-KEY ПРОТЕКЦІЯ
# ======================================================
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != "your-secret-api-key-here":
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated


# ======================================================
#   РЕЄСТРАЦІЯ ВСІХ API-МАРШРУТІВ
# ======================================================
def setup_api_routes(app, db):

    # ==================================================
    #                    BOOKS API
    # ==================================================
    @app.route('/api/books', methods=['GET'])
    @require_api_key
    def api_books():
        query = """
            SELECT 
                b.book_id, b.book_name, b.isbn, b.publication_year,
                b.price, b.stock_quantity, a.name AS author,
                COALESCE(string_agg(c.category_name, ', ' ORDER BY c.category_name), '')
            FROM books b
            INNER JOIN authors a ON b.author_id = a.author_id
            LEFT JOIN books_categories bc ON b.book_id = bc.book_id
            LEFT JOIN categories c ON bc.category_id = c.category_id
            GROUP BY b.book_id, a.name
            ORDER BY b.book_name;
        """
        cur = db.execute_query(query)
        books = cur.fetchall() if cur else []

        return jsonify({
            "success": True,
            "count": len(books),
            "data": [
                {
                    "id": b[0],
                    "title": b[1],
                    "isbn": b[2],
                    "year": b[3],
                    "price": float(b[4]),
                    "stock": b[5],
                    "author": b[6],
                    "categories": b[7]
                }
                for b in books
            ]
        })

    @app.route("/api/books/<int:book_id>", methods=['GET'])
    @require_api_key
    def api_book_detail(book_id):
        query = """
            SELECT 
                b.book_id, b.book_name, b.isbn, b.publication_year,
                b.price, b.stock_quantity, a.name
            FROM books b
            INNER JOIN authors a ON b.author_id = a.author_id
            WHERE b.book_id = %s;
        """
        cur = db.execute_query(query, (book_id,))
        book = cur.fetchone() if cur else None

        if not book:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({
            "success": True,
            "data": {
                "id": book[0],
                "title": book[1],
                "isbn": book[2],
                "year": book[3],
                "price": float(book[4]),
                "stock": book[5],
                "author": book[6]
            }
        })

    @app.route("/api/books", methods=['POST'])
    @require_api_key
    def api_create_book():
        data = request.json

        required = ["book_name", "isbn", "publication_year", "price", "stock_quantity", "author_id"]
        if not all(f in data for f in required):
            return jsonify({"error": "Missing fields"}), 400

        cur = db.execute_query("""
            INSERT INTO books (book_name, isbn, publication_year, price, stock_quantity, author_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING book_id;
        """, (
            data["book_name"], data["isbn"], data["publication_year"],
            data["price"], data["stock_quantity"], data["author_id"]
        ))

        book_id = cur.fetchone()[0]
        return jsonify({"success": True, "book_id": book_id}), 201

    @app.route("/api/books/<int:book_id>", methods=['PATCH'])
    @require_api_key
    def api_update_book(book_id):
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        allowed = ["book_name", "isbn", "publication_year", "price", "stock_quantity", "author_id"]
        fields = []
        values = []

        for key, value in data.items():
            if key in allowed:
                fields.append(f"{key} = %s")
                values.append(value)

        if not fields:
            return jsonify({"error": "No valid fields"}), 400

        values.append(book_id)

        cur = db.execute_query(
            f"UPDATE books SET {', '.join(fields)} WHERE book_id = %s;",
            values
        )

        return jsonify({"success": True, "updated": book_id})

    @app.route("/api/books/<int:book_id>", methods=['DELETE'])
    @require_api_key
    def api_delete_book(book_id):
        db.execute_query("DELETE FROM books_categories WHERE book_id = %s", (book_id,))
        cur = db.execute_query("DELETE FROM books WHERE book_id = %s", (book_id,))

        return jsonify({"success": True, "deleted": book_id})

    # ==================================================
    #                   AUTHORS API
    # ==================================================
    @app.route("/api/authors", methods=['GET'])
    @require_api_key
    def api_authors():
        cur = db.execute_query("SELECT author_id, name, birth_year, country FROM authors ORDER BY name")
        authors = cur.fetchall() if cur else []

        return jsonify({
            "success": True,
            "count": len(authors),
            "data": [
                {"id": a[0], "name": a[1], "birth_year": a[2], "country": a[3]}
                for a in authors
            ]
        })

    @app.route("/api/authors/<int:author_id>", methods=['GET'])
    @require_api_key
    def api_author_detail(author_id):
        cur = db.execute_query(
            "SELECT author_id, name, birth_year, country FROM authors WHERE author_id = %s",
            (author_id,)
        )
        author = cur.fetchone() if cur else None

        if not author:
            return jsonify({"error": "Author not found"}), 404

        return jsonify({
            "success": True,
            "data": {
                "id": author[0],
                "name": author[1],
                "birth_year": author[2],
                "country": author[3]
            }
        })

    @app.route("/api/authors", methods=['POST'])
    @require_api_key
    def api_create_author():
        data = request.json

        if "name" not in data:
            return jsonify({"error": "Missing field: name"}), 400

        cur = db.execute_query("""
            INSERT INTO authors (name, birth_year, country)
            VALUES (%s, %s, %s)
            RETURNING author_id;
        """, (
            data["name"],
            data.get("birth_year"),
            data.get("country")
        ))

        author_id = cur.fetchone()[0]
        return jsonify({"success": True, "author_id": author_id}), 201

    @app.route("/api/authors/<int:author_id>", methods=['PATCH'])
    @require_api_key
    def api_update_author(author_id):
        data = request.json
        allowed = ["name", "birth_year", "country"]

        fields = []
        values = []

        for k, v in data.items():
            if k in allowed:
                fields.append(f"{k} = %s")
                values.append(v)

        if not fields:
            return jsonify({"error": "No valid fields"}), 400

        values.append(author_id)

        db.execute_query(
            f"UPDATE authors SET {', '.join(fields)} WHERE author_id = %s",
            values
        )

        return jsonify({"success": True, "updated": author_id})

    @app.route("/api/authors/<int:author_id>", methods=['DELETE'])
    @require_api_key
    def api_delete_author(author_id):
        cur = db.execute_query("DELETE FROM authors WHERE author_id = %s", (author_id,))
        return jsonify({"success": True, "deleted": author_id})

    # ==================================================
    #                 CATEGORIES API
    # ==================================================
    @app.route("/api/categories", methods=['GET'])
    @require_api_key
    def api_categories():
        cur = db.execute_query("SELECT category_id, category_name FROM categories ORDER BY category_name")
        rows = cur.fetchall() if cur else []

        return jsonify({
            "success": True,
            "count": len(rows),
            "data": [{"id": c[0], "name": c[1]} for c in rows]
        })

    @app.route("/api/categories/<int:category_id>", methods=['GET'])
    @require_api_key
    def api_category_detail(category_id):
        cur = db.execute_query(
            "SELECT category_id, category_name FROM categories WHERE category_id = %s",
            (category_id,)
        )
        cat = cur.fetchone() if cur else None

        if not cat:
            return jsonify({"error": "Category not found"}), 404

        return jsonify({
            "success": True,
            "data": {"id": cat[0], "name": cat[1]}
        })

    @app.route("/api/categories", methods=['POST'])
    @require_api_key
    def api_create_category():
        data = request.json

        if "category_name" not in data:
            return jsonify({"error": "Missing field: category_name"}), 400

        cur = db.execute_query("""
            INSERT INTO categories (category_name)
            VALUES (%s)
            RETURNING category_id;
        """, (data["category_name"],))

        cid = cur.fetchone()[0]
        return jsonify({"success": True, "category_id": cid}), 201

    @app.route("/api/categories/<int:category_id>", methods=['PATCH'])
    @require_api_key
    def api_update_category(category_id):
        data = request.json

        if "category_name" not in data:
            return jsonify({"error": "Missing category_name"}), 400

        db.execute_query(
            "UPDATE categories SET category_name = %s WHERE category_id = %s",
            (data["category_name"], category_id)
        )

        return jsonify({"success": True, "updated": category_id})

    @app.route("/api/categories/<int:category_id>", methods=['DELETE'])
    @require_api_key
    def api_delete_category(category_id):
        db.execute_query("DELETE FROM books_categories WHERE category_id = %s", (category_id,))
        db.execute_query("DELETE FROM categories WHERE category_id = %s", (category_id,))

        return jsonify({"success": True, "deleted": category_id})
