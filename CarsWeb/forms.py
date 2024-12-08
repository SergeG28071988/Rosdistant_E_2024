from email_validator import validate_email, EmailNotValidError
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, FileField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email

from models import Rental


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        try:
            # Валидация email
            valid_email = validate_email(email.data)
            email.data = valid_email['email']  # нормализованный адрес
        except EmailNotValidError as e:
            raise ValidationError(str(e))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        try:
            # Валидация email
            valid_email = validate_email(email.data)
            email.data = valid_email['email']  # нормализованный адрес
        except EmailNotValidError as e:
            raise ValidationError(str(e))
        

class RentalForm(FlaskForm):
    renter_name = StringField('Арендатор', validators=[DataRequired()])
    car_model = StringField('Модель автомобиля', validators=[DataRequired()])
    car_photo = FileField('Фото автомобиля')
    rental_date = DateField('Дата аренды', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Дата возврата автомобиля', format='%Y-%m-%d', validators=[DataRequired()])
    rental_category = SelectField('Категория', choices=Rental.CATEGORY_CHOICES)
    rental_duration = IntegerField('Длительность аренды (в днях)', validators=[DataRequired()])
    rental_cost = FloatField('Стоимость аренды', validators=[DataRequired()])
        

class SearchForm(FlaskForm):
    renter_name = StringField('Арендатор')
    submit = SubmitField('Поиск')
    clear = SubmitField('Очистить поиск')  # Новое поле для очистки


# Форма для отправки сообщений
class MessageForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')
