import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ---------------------------------------------
# ПІДКЛЮЧЕННЯ УКРАЇНСЬКОГО ШРИФТУ
# ---------------------------------------------
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("DejaVu", FONT_PATH))
    DEFAULT_FONT = "DejaVu"
else:
    DEFAULT_FONT = "Helvetica"


# ---------------------------------------------
# ГОЛОВНА ФУНКЦІЯ
# ---------------------------------------------
def generate_books_report(books):

    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    filename = os.path.join(reports_dir, "books_report.pdf")

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # ---------------------------------------------
    # Заголовок
    # ---------------------------------------------
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontName=DEFAULT_FONT,
        fontSize=26,
        textColor=colors.HexColor("#3f3b3d"),
        alignment=1,
        spaceAfter=25
    )

    elements.append(Paragraph("Звіт про книги", title_style))

    date_style = ParagraphStyle(
        'DateStyle',
        fontName=DEFAULT_FONT,
        fontSize=11,
        textColor=colors.HexColor("#66678b"),
        alignment=1
    )

    elements.append(Paragraph(
        f"Дата формування: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        date_style
    ))
    elements.append(Spacer(1, 15))

    # ---------------------------------------------
    # Таблиця
    # ---------------------------------------------
    table_data = [["№", "Назва", "ISBN", "Рік", "Ціна", "Автор"]]

    # Стиль для комірок з переносом
    cell_style = ParagraphStyle(
        'CellStyle',
        fontName=DEFAULT_FONT,
        fontSize=10,
        leading=12,
        textColor=colors.whitesmoke
    )

    for idx, book in enumerate(books, 1):

        book_name = Paragraph(str(book[1]), cell_style)
        author_name = Paragraph(str(book[6]), cell_style)

        row = [
            str(idx),
            book_name,
            str(book[2]),
            str(book[3]),
            f"{book[4]:.2f}",
            author_name
        ]

        table_data.append(row)

    # Ширини колонок
    col_widths = [
        0.5 * inch,   # №
        2.8 * inch,   # Назва
        1.4 * inch,   # ISBN
        0.8 * inch,   # Рік
        0.9 * inch,   # Ціна
        1.8 * inch    # Автор
    ]

    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([
        # Заголовок
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#11131b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#fcd2e0')),
        ('FONTNAME', (0, 0), (-1, 0), DEFAULT_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Тіло таблиці
        ('FONTNAME', (0, 1), (-1, -1), DEFAULT_FONT),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
        ('FONTSIZE', (0, 1), (-1, -1), 10),

        # Темні рядки
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#181b27')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#181b27'),
            colors.HexColor('#202437')
        ]),

        # Рамка
        ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#2b3045')),

        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)

    # ---------------------------------------------
    # Статистика
    # ---------------------------------------------
    elements.append(Spacer(1, 25))

    total_books = len(books)
    total_price = sum(b[4] for b in books)
    avg_price = total_price / total_books if total_books else 0

    stats_style = ParagraphStyle(
        'StatsStyle',
        fontName=DEFAULT_FONT,
        fontSize=12,
        textColor=colors.HexColor("#3f3b3d"),
        leading=14
    )

    stats_text = f"""
    <b>Статистика:</b><br/>
    Всього книг: {total_books}<br/>
    Загальна вартість: {total_price:.2f} грн<br/>
    Середня ціна: {avg_price:.2f} грн
    """

    elements.append(Paragraph(stats_text, stats_style))

    # ---------------------------------------------
    # Генерація PDF
    # ---------------------------------------------
    doc.build(elements)

    return filename
