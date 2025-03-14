from flask import Blueprint, render_template , request
from flask_login import login_required
from app import db
import random
from app.database.models import Product
from app.wraps import admin_required

admin = Blueprint("admin", __name__)

@admin.route("/test")
def test():
    try:
        # for i in range(100):
        #     name = "product" + str(i)  # Додаємо `str(i)`, щоб конкатенація працювала
        #     price = random.randint(100, 1000)
        #     image = "app/static/image/image.jpg"
        #     description = "description" + str(i)  # Аналогічно додаємо `str(i)`
        #     stock = random.randint(1, 100)
        #     category = "test"  # Виправлено `categoty` → `category`
        #
        #     new_product = Product(
        #         name=name,
        #         price=price,
        #         image=image,
        #         description=description,
        #         stock=stock,
        #         category=category
        #     )
        #     db.session.add(new_product)

        products = Product.query.all()

        # Проходимось по кожному продукту
        for i, product in enumerate(products, start=1):
            product.image = "image/image.jpg"  # Новий шлях до зображення
        db.session.commit()
        print("Продукти успішно додані!")
    except Exception as e:
        db.session.rollback()
        print(f"Помилка: {e}")
    finally:
        db.session.close()
        return "This is a test response"


@admin.route("/dashboard")
@admin_required
def dashboard():
    return render_template("admin/base.html")



