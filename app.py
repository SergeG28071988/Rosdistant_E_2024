from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm, MessageForm  # Создайте эти формы
from forms import RentalForm, SearchForm
from models import db, User, Rental, Message  # Добавьте импорт модели User
from werkzeug.utils import secure_filename
import os


app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_cars.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'  # Папка для сохранения загруженных изображений
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Укажите страницу входа


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))  # Или другую страницу после входа
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    search_form = SearchForm(request.form)

    # Обработка формы поиска
    if search_form.validate_on_submit():
        if search_form.clear.data:  # Если нажата кнопка "Очистить поиск"
            search_form.renter_name.data = ''  # Очищаем поле ввода фамилии
            rentals = Rental.query.order_by(Rental.rental_cost).all()
        else:
            # Логика поиска по арендатору
            renter_name = search_form.renter_name.data
            rentals = Rental.query.filter(Rental.renter_name.contains(renter_name)).all()
    else:
        rentals = Rental.query.order_by(Rental.rental_cost).all()
    return render_template("rentals.html", rentals=rentals, search_form=search_form)


@app.route('/add_rental', methods=['POST', 'GET'])
def add_rental():
    form = RentalForm()

    if form.validate_on_submit():
        # Обработка загрузки файла
        car_photo_filename = None
        if form.car_photo.data:
            file = form.car_photo.data
            car_photo_filename = secure_filename(file.filename)  # Безопасное имя файла
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], car_photo_filename))  # Сохранение файла

        # Создание нового объекта аренды
        new_rental = Rental(
            renter_name=form.renter_name.data,
            car_model=form.car_model.data,
            car_photo=car_photo_filename,  # Сохраняем имя файла
            rental_date=form.rental_date.data,
            return_date=form.return_date.data,
            rental_category=form.rental_category.data,
            rental_duration=form.rental_duration.data,
            rental_cost=form.rental_cost.data
        )

        # Добавление в базу данных
        db.session.add(new_rental)
        db.session.commit()
        flash('Аренда успешно добавлена!', 'success')
        return redirect(url_for('rentals'))

    return render_template('add_rental.html', form=form)


@app.route('/rentals/<int:id>')
def rental_detail(id):
    rental = Rental.query.get(id)
    return render_template("rental_detail.html", rental=rental)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/rentals/<int:id>/edit', methods=['POST', 'GET'])
def rental_edit(id):
    rental = Rental.query.get(id)
    if not rental:
        return "Запись не найдена", 404

    if request.method == 'POST':
        rental.renter_name = request.form['renter_name']
        rental.car_model = request.form['car_model']

        # Обработка загрузки фото
        if 'car_photo' in request.files:
            file = request.files['car_photo']
            if file and allowed_file(file.filename):  # Предполагается, что у вас есть функция allowed_file
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                rental.car_photo = filename  # Сохраняем имя файла в базе данных

        rental.rental_date = datetime.strptime(request.form['rental_date'], '%Y-%m-%d')
        rental.return_date = datetime.strptime(request.form['return_date'], '%Y-%m-%d')
        rental.rental_category = request.form['rental_category']
        rental.rental_duration = int(request.form['rental_duration'])
        rental.rental_cost = float(request.form['rental_cost'])

        try:
            db.session.commit()
            return redirect(url_for('rentals'))
        except Exception as e:
            return f"При изменении записи аренды произошла ошибка: {str(e)}"

    form = RentalForm(obj=rental)  # Предполагается, что у вас есть форма RentalForm
    return render_template("rental_edit.html", rental=rental, form=form)


@app.route('/rentals/<int:id>/delete')
def rental_delete(id):
    rental = Rental.query.get_or_404(id)

    try:
        db.session.delete(rental)
        db.session.commit()
        return redirect('/rentals')
    except Exception as e:
        return f"При удалении записи аренды произошла ошибка: {str(e)}"


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/messages', methods=['GET'])
def show_messages():
    messages = Message.query.all()  # Получаем все сообщения из базы данных
    return render_template('messages.html', messages=messages)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MessageForm()
    if form.validate_on_submit():
        # Сохраняем сообщение в базе данных
        new_message = Message(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Мы получили ваше обращение и скоро свяжемся с вами.')
        return redirect('/contact')

    return render_template('contact.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
