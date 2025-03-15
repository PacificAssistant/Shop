import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://shop_user:31049902@localhost/shop_db'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app/static/image")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB ліміт на файл

