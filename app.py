from flask import Flask, render_template, request, jsonify, abort, url_for
from markupsafe import escape

app = Flask(__name__)

# 1. Danh sách dữ liệu mẫu (>= 4 cuốn)
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python Căn Bản",
        "author": "Nguyễn Văn A",
        "year": 2022,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Miguel Grinberg",
        "year": 2018,
        "category": "Lập trình",
        "available": False
    },
    {
        "id": 3,
        "title": "Cấu Trúc Dữ Liệu và Giải Thuật",
        "author": "Trần Văn B",
        "year": 2020,
        "category": "Khoa học máy tính",
        "available": True
    },
    {
        "id": 4,
        "title": "Thấu Hiểu Tiếp Thị",
        "author": "Philip Kotler",
        "year": 2019,
        "category": "Kinh tế",
        "available": True
    },
    {
        "id": 5,
        "title": "Thiết Kế Cơ Sở Dữ Liệu",
        "author": "Lê Văn C",
        "year": 2021,
        "category": "Khoa học máy tính",
        "available": False
    }
]

# Hàm hỗ trợ tìm sách theo ID
def find_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

# 2. Route Trang chủ /
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = len([b for b in BOOKS if b["available"]])
    return render_template("index.html", total_books=total_books, available_books=available_books)

# 3. Route Danh sách sách /books (Hỗ trợ lọc ?category=...)
@app.route("/books")
def books_list():
    category = request.args.get("category", "").strip()
    
    # Lấy danh sách các thể loại duy nhất để làm thanh lọc
    categories = sorted(list(set(b["category"] for b in BOOKS)))
    
    if category:
        filtered_books = [b for b in BOOKS if b["category"].lower() == category.lower()]
    else:
        filtered_books = BOOKS

    return render_template(
        "books.html", 
        books=filtered_books, 
        categories=categories, 
        selected_category=category
    )

# 4. Route Chi tiết sách /books/<int:book_id>
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = find_book(book_id)
    if not book:
        # Tự động chuyển qua trang 404 kèm thông điệp
        abort(404, description=f"Không có sách với ID = {escape(str(book_id))}")
    
    return render_template("book_detail.html", book=book)

# 5. API Routes
@app.route("/api/books", methods=["GET"])
def api_books():
    category = request.args.get("category", "").strip()
    if category:
        filtered = [b for b in BOOKS if b["category"].lower() == category.lower()]
        return jsonify(filtered)
    return jsonify(BOOKS)

@app.route("/api/books/<int:book_id>", methods=["GET"])
def api_book_detail(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": f"Không có sách với ID = {book_id}"}), 404
    return jsonify(book)

# 6. Trang 404 tùy biến (Phân biệt giữa API và HTML)
@app.errorhandler(404)
def page_not_found(error):
    # Nếu truy cập API bị lỗi 404
    if request.path.startswith("/api/"):
        msg = getattr(error, 'description', 'Endpoint không tồn tại')
        return jsonify({"error": msg}), 404
    
    # Giao diện HTML 404
    message = getattr(error, 'description', 'Trang không tồn tại')
    return render_template("404.html", message=message), 404

if __name__ == "__main__":
    app.run(debug=True)