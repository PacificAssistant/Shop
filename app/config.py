import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://shop_user:31049902@localhost/shop_db'
