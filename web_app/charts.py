import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def create_author_statistics_chart(db):
    query = """
        SELECT 
            a.name AS full_name,
            COUNT(b.book_id) AS books_count
        FROM authors a
        LEFT JOIN books b ON a.author_id = b.author_id
        GROUP BY a.author_id, full_name
        ORDER BY books_count DESC
        LIMIT 10;
    """
    cursor = db.execute_query(query)
    data = cursor.fetchall() if cursor else []

    if not data:
        return None

    authors = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(authors, counts, color='#f7a8b8')

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha='center', va='bottom'
        )

    plt.xlabel('Автори', fontsize=12)
    plt.ylabel('Кількість книг', fontsize=12)
    plt.title('Топ-10 авторів за кількістю книг', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=110, bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return encoded



def create_price_distribution_chart(db):
    query = "SELECT price FROM books ORDER BY price;"
    cursor = db.execute_query(query)
    data = cursor.fetchall() if cursor else []

    if not data:
        return None

    prices = [row[0] for row in data]

    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=12, color='#9ad0c2', edgecolor='black', alpha=0.75)

    plt.xlabel('Ціна (грн)', fontsize=12)
    plt.ylabel('Кількість книг', fontsize=12)
    plt.title('Розподіл цін на книги', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=110, bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return encoded
