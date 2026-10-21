import math
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
    "open": 7,
    "close": 22,
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai",
]

# Danh sách 7 món theo đề bài bài 3 & 4
MENU = [
    {
        "id": 1,
        "name": "cà phê đen",
        "price": 20000,
        "available": True,
        "image": "ca-phe-den.jpg",
    },
    {
        "id": 2,
        "name": "cà phê sữa",
        "price": 25000,
        "available": True,
        "image": "ca-phe-sua.jpg",
    },
    {
        "id": 3,
        "name": "bạc xỉu",
        "price": 30000,
        "available": False,
        "image": "bac-xiu.jpg",
    },
    {
        "id": 4,
        "name": "trà đào",
        "price": 35000,
        "available": True,
        "image": "tra-dao.jpg",
    },
    {
        "id": 5,
        "name": "trà sữa",
        "price": 35000,
        "available": True,
        "image": "tra-sua.jpg",
    },
    {
        "id": 6,
        "name": "nước cam",
        "price": 30000,
        "available": True,
        "image": "nuoc-cam.jpg",
    },
    {
        "id": 7,
        "name": "sinh tố bơ",
        "price": 40000,
        "available": True,
        "image": "sinh-to-bo.jpg",
    },
]


@app.template_filter("vnd")
def format_vnd(value):
    if value is None:
        return "0 đ"
    return f"{int(value):,}".replace(",", ".") + " đ"


@app.route("/")
def index():
    gio_param = request.args.get("gio")
    current_hour = (
        int(gio_param)
        if gio_param and gio_param.isdigit()
        else datetime.now().hour
    )
    is_open = SHOP["open"] <= current_hour < SHOP["close"]

    return render_template(
        "trangchu.html",
        shop=SHOP,
        promotions=PROMOTIONS,
        current_hour=current_hour,
        is_open=is_open,
    )


# Route /menu hỗ trợ phân trang page=N (Mỗi trang 3 món)
@app.route("/menu")
def show_menu():
    per_page = 3
    total_items = len(MENU)
    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 1

    # Lấy tham số page từ URL
    page_param = request.args.get("page", 1)

    try:
        page = int(page_param)
    except ValueError:
        return render_template("404.html"), 404

    # Nếu page < 1 hoặc vượt quá số trang thực tế -> 404 Not Found
    if page < 1 or (page > total_pages and total_items > 0):
        return render_template("404.html"), 404

    # Cắt danh sách món theo trang
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    items_on_page = MENU[start_idx:end_idx]

    return render_template(
        "menu.html",
        menu=items_on_page,
        page=page,
        total_pages=total_pages,
    )


@app.route("/contact")
def contact():
    return render_template("contact.html", shop=SHOP)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)