from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
import random
from app.database.models import Product, Category
from app.wraps import admin_required
from app.forms import ProductForm, CategoryForm
from flask import flash ,redirect, url_for
from werkzeug.utils import secure_filename
import os
from app.config import Config
from app.database.models import Product



admin = Blueprint("admin", __name__)
@admin.route("/changeRecord", methods=["GET", "POST"])
@admin_required
def change_record():
    products = Product.query.all()
    return render_template("admin/changeRecord.html", products=products)


@admin.route("/get_product/<int:product_id>")
@admin_required
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "description": product.description
        })
    return jsonify({"error": "Продукт не знайдено"}), 404


@admin.route("/update_product", methods=["POST"])
@admin_required
def update_product():
    product_id = request.form.get("product_id")
    product = Product.query.get(product_id)

    if product:
        product.name = request.form.get("name")
        product.price = float(request.form.get("price"))
        product.stock = int(request.form.get("stock"))
        product.description = request.form.get("description")
        db.session.commit()
        return jsonify({"message": "Продукт оновлено!"})

    return jsonify({"error": "Помилка оновлення"}), 400


@admin.route("/test3")
@admin_required
def test_one():
    try:
        for i in range(100):
            product = Product(  # Створюємо об'єкт моделі Product, а не форми
                name=f"product {i}",
                price=random.randint(100, 10000),
                image="image/image.jpg",
                description=f"descriptions {i}",
                stock=random.randint(2, 100),
                category_id="2900d125-3ddc-4e92-b52a-ff7ac6ad4935"
            )
            db.session.add(product)
        db.session.commit()
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


@admin.route("/addRecord", methods=["GET", "POST"])
@admin_required
def add_record():
    product_form = ProductForm()
    category_form = CategoryForm()

    if product_form.submit.data and product_form.validate_on_submit():
        image_filename = "default.jpg"

        if product_form.image.data:
            try:
                image_filename = secure_filename(product_form.image.data.filename)

                UPLOAD_FOLDER = Config.UPLOAD_FOLDER

                # Створюємо повний шлях для збереження
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)

                # Створюємо папку, якщо її немає
                if not os.path.exists(UPLOAD_FOLDER):
                    print("Створюю папку:", UPLOAD_FOLDER)
                    os.makedirs(UPLOAD_FOLDER)
                print("Файл для збереження:", image_filename)
                print(product_form.image)

                # Зберігаємо файл
                product_form.image.data.save(image_path)
                print(image_path)

                # Записуємо правильний шлях у базу (відносно static/)
                saved_image_path = f"image/{image_filename}"

            except Exception as e:
                print("Помилка при збереженні файлу:", e)
                flash("Помилка при збереженні файлу.", "error")

        else:
            saved_image_path = "image/default.jpg"  # Якщо немає файлу, ставимо заглушку

        product = Product(
            name=product_form.name.data,
            price=product_form.price.data,
            image=saved_image_path,
            description=product_form.description.data,
            stock=product_form.stock.data,
            category_id=product_form.category.data
        )

        db.session.add(product)
        db.session.commit()
        flash("Продукт додано успішно!", "success")
        return redirect(url_for("admin.add_record"))

    if category_form.submit.data and category_form.validate_on_submit():
        existing_category = Category.query.filter_by(name=category_form.name.data).first()
        if existing_category:
            flash("Така категорія вже існує!", "danger")
        else:
            new_category = Category(name=category_form.name.data)
            db.session.add(new_category)
            db.session.commit()
            flash("Категорію успішно додано!", "success")

        return redirect(url_for("admin.add_record"))
    categories = Category.query.all()
    return render_template("admin/addRecord.html", product_form=product_form, category_form=category_form,
                           categories=categories)
