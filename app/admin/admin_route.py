import os
from flask import render_template, request, jsonify, redirect, url_for, flash,Blueprint
from werkzeug.utils import secure_filename

from app.wraps import admin_required
from app.forms import ProductForm, CategoryForm
from app.admin.admin_class import ProductService,CategoryService
from app.config import Config

admin = Blueprint("admin", __name__)
@admin.route("/changeRecord", methods=["GET", "POST"])
@admin_required
def change_record():
    products = ProductService.get_all_products()
    return render_template("admin/changeRecord.html", products=products)


@admin.route("/get_product/<int:product_id>")
@admin_required
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
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
    name = request.form.get("name")
    price = request.form.get("price")
    stock = request.form.get("stock")
    description = request.form.get("description")

    product = ProductService.update_product(product_id, name, price, stock, description)

    if product:
        return jsonify({"message": "Продукт оновлено!"})

    return jsonify({"error": "Помилка оновлення"}), 400


@admin.route("/test3")
@admin_required
def test_one():
    ProductService.bulk_add_products()
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
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)

                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                product_form.image.data.save(image_path)
                saved_image_path = f"image/{image_filename}"

            except Exception as e:
                flash("Помилка при збереженні файлу.", "error")
                saved_image_path = "image/default.jpg"

        else:
            saved_image_path = "image/default.jpg"

        ProductService.add_product(
            name=product_form.name.data,
            price=product_form.price.data,
            image=saved_image_path,
            description=product_form.description.data,
            stock=product_form.stock.data,
            category_id=product_form.category.data
        )

        flash("Продукт додано успішно!", "success")
        return redirect(url_for("admin.add_record"))

    if category_form.submit.data and category_form.validate_on_submit():
        category = CategoryService.add_category(category_form.name.data)
        if category:
            flash("Категорію успішно додано!", "success")
        else:
            flash("Така категорія вже існує!", "danger")

        return redirect(url_for("admin.add_record"))

    categories = CategoryService.get_all_categories()
    return render_template("admin/addRecord.html", product_form=product_form, category_form=category_form,
                           categories=categories)
