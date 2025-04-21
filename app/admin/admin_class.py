import random
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.database.models import Product, Category


class ProductService:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id, name, price, stock, description):
        """Оновлює дані продукту за його ID."""
        product = Product.query.get(product_id)
        if not product:
            return None  # Повертаємо None, якщо продукт не знайдено

        try:
            product.name = name
            product.price = float(price) if price is not None else product.price
            product.stock = int(stock) if stock is not None else product.stock
            product.description = description if description else product.description

            db.session.commit()
            return product
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()  # Відкат змін у разі помилки
            print(f"Помилка оновлення продукту: {e}")
            return None

    @staticmethod
    def add_product(name, price, image, description, stock, category_id):
        """Додає новий продукт у базу даних."""
        try:
            product = Product(
                name=name,
                price=float(price),
                image=image if image else "image/default.jpg",
                description=description if description else "",
                stock=int(stock),
                category_id=category_id
            )

            db.session.add(product)
            db.session.commit()
            return product
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()  # Відкат у разі помилки
            print(f"Помилка додавання продукту: {e}")
            return None

    @staticmethod
    def bulk_add_products():
        try:
            for i in range(100):
                product = Product(
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


class CategoryService:
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def add_category(name):
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return None
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category
