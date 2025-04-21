from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange,Length
from flask_wtf.file import FileField, FileRequired


class ProductForm(FlaskForm):
    name = StringField("Назва", validators=[DataRequired()])
    price = FloatField("Ціна", validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Зображення', validators=[FileRequired()])
    description = TextAreaField("Опис")
    stock = IntegerField("Кількість на складі", validators=[DataRequired(), NumberRange(min=0)])
    category = StringField("Категорія")
    submit = SubmitField("Додати продукт")


class CategoryForm(FlaskForm):
    name = StringField("Назва категорії", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField("Додати категорію")

