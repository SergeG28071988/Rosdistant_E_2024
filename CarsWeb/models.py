from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    renter_name = db.Column(db.String(100), nullable=False,
                            info={'help_text': 'Введите арендатора', 'verbose_name': 'Арендатор'})
    car_model = db.Column(db.String(100), nullable=False,
                           info={'help_text': 'Введите модель', 'verbose_name': 'Модель авто'})
    car_photo = db.Column(db.String(200), nullable=True)  # Путь к изображению
    rental_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc),
                            info={'help_text': 'Введите дату аренды', 'verbose_name': 'Дата аренды'})
    return_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc),
                            info={'help_text': 'Введите дату возврата авто', 'verbose_name': 'Дата возврата авто'})
    CATEGORY_CHOICES = [
        ('', 'Выберите категорию'),
        ('Долгосрочная', 'Долгосрочная'),
        ('Краткосрочная', 'Краткосрочная'),
    ]
    rental_category = db.Column(db.String(50), nullable=False,
                                info={'verbose_name': 'Категория'})  # краткосрочная или долгосрочная
    rental_duration = db.Column(db.Integer, nullable=False,
                                info={'help_text': 'Введите длительность аренды', 'verbose_name': 'Длительность аренды'})  # в днях
    rental_cost = db.Column(db.Float, nullable=False,
                            info={'help_text': 'Введите стоимость аренды', 'verbose_name': 'Стоимость аренды'})

    def __repr__(self):
        return f'<Rental {self.renter_name}, {self.bike_model}>'
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, info={'help_text': 'Введите имя', 'verbose_name': 'Имя'})
    phone = db.Column(db.String(15), nullable=False, info={'help_text': 'Введите телефон', 'verbose_name': 'Телефон'})
    email = db.Column(db.String(120), nullable=False, info={'help_text': 'Введите Email', 'verbose_name': 'Email'})
    message = db.Column(db.Text, nullable=False, info={'help_text': 'Введите сообщение', 'verbose_name': 'Сообщение'})
    