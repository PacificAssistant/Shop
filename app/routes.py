from flask import Blueprint, render_template , request
from flask_login import login_required
from app import db
from app.database.models import Product

main = Blueprint("main", __name__)

@main.route("/",methods=["GET"])
def home():
    products = Product.query.with_entities(Product.name, Product.image,Product.id).all()
    return render_template("index.html",products=products)

@main.route("/product/<int:product_id>", methods=["GET"])
def product(product_id):
    product = Product.query.get(product_id)


    if not product:
        return "Товар не знайдено", 404
    return render_template("product.html", product=product)



