from flask import Flask, render_template, request, redirect, url_for, flash, session,Blueprint
from flask_login import login_required
from app import db, current_user
from app.database.models import Product, User, Order, OrderItem
import uuid

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def home():
    products = Product.query.with_entities(Product.name, Product.image, Product.id).all()
    return render_template("index.html", products=products)


@main.route("/product/<string:product_id>", methods=["GET"])
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()

    product_dict = product.to_dict()

    if not product:
        return "Товар не знайдено", 404
    return render_template("product.html", product=product_dict)


@main.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        cart_data = request.form.get("cartData")  # Отримуємо JSON з кошиком

        if not cart_data:
            return "Помилка: Кошик порожній", 400

        cart = eval(cart_data)  # Перетворюємо JSON-рядок у список (краще використовувати `json.loads`)

        print(f"Ім'я: {name}, Email: {email}, Адреса: {address}, Кошик: {cart}")

        total_price = sum(item["price"] * item["quantity"] for item in cart)
        order_number = f"ORD{str(uuid.uuid4())[:16]}"

        new_order = Order(
            order_number=order_number,
            user_id=current_user.id,
            total_price=total_price,
            status="Очікує оплату"
        )
        db.session.add(new_order)
        db.session.commit()

        for item in cart:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item["id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            db.session.add(order_item)

        db.session.commit()
        session.pop("cart", None)  # Очищаємо кошик після замовлення
        flash("Замовлення успішно оформлено!", "success")
        return redirect(url_for("main.home"))
    return render_template("checkout.html")



