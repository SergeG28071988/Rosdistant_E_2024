import telebot
import sqlite3
from config import TOKEN  # Импортируем токен из config.py

bot = telebot.TeleBot(TOKEN)

# Функция для создания базы данных
def create_database():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            year INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления автомобиля
def add_car(brand, year, price):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cars (brand, year, price) VALUES (?, ?, ?)', (brand, year, price))
    conn.commit()
    conn.close()

# Функция для получения списка автомобилей
def get_cars():
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return cars

# Функция для редактирования автомобиля
def edit_car(car_id, brand, year, price):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE cars SET brand=?, year=?, price=? WHERE id=?', (brand, year, price, car_id))
    conn.commit()
    conn.close()

# Функция для удаления автомобиля
def delete_car(car_id):
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cars WHERE id=?', (car_id,))
    conn.commit()
    conn.close()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Показать автомобили", "Добавить автомобиль", "Редактировать автомобиль", "Удалить автомобиль")
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "Показать автомобили":
        list_cars(message)
    elif message.text == "Добавить автомобиль":
        add_car_command(message)
    elif message.text == "Редактировать автомобиль":
        edit_car_command(message)
    elif message.text == "Удалить автомобиль":
        delete_car_command(message)

# Обработчик команды /add
def add_car_command(message):
    msg = bot.send_message(message.chat.id, "Введите марку автомобиля:")
    bot.register_next_step_handler(msg, process_brand_step)

def process_brand_step(message):
    brand = message.text
    msg = bot.send_message(message.chat.id, "Введите год выпуска:")
    bot.register_next_step_handler(msg, process_year_step, brand)

def process_year_step(message, brand):
    year = message.text
    msg = bot.send_message(message.chat.id, "Введите цену:")
    bot.register_next_step_handler(msg, process_price_step, brand, year)

def process_price_step(message, brand, year):
    price = message.text
    add_car(brand, year, price)
    bot.send_message(message.chat.id, "Автомобиль добавлен!")

# Обработчик команды /list
def list_cars(message):
    cars = get_cars()
    if cars:
        response = "\n".join([f"{car[0]}: {car[1]}, {car[2]}, {car[3]} руб." for car in cars])
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Список автомобилей пуст. Пожалуйста, добавьте автомобиль используя команду 'Добавить автомобиль'.")

# Обработчик команды редактирования
def edit_car_command(message):
    msg = bot.send_message(message.chat.id, "Введите ID автомобиля для редактирования:")
    bot.register_next_step_handler(msg, process_edit_id_step)

def process_edit_id_step(message):
    car_id = message.text
    cars = get_cars()
    
    # Проверка существования автомобиля
    if any(str(car[0]) == car_id for car in cars):
                msg = bot.send_message(message.chat.id, "Введите новую марку автомобиля:")
                bot.register_next_step_handler(msg, process_edit_brand_step, car_id)
    else:
        bot.send_message(message.chat.id, "Автомобиль с таким ID не найден.")

def process_edit_brand_step(message, car_id):
    brand = message.text
    msg = bot.send_message(message.chat.id, "Введите новый год выпуска:")
    bot.register_next_step_handler(msg, process_edit_year_step, car_id, brand)

def process_edit_year_step(message, car_id, brand):
    year = message.text
    msg = bot.send_message(message.chat.id, "Введите новую цену:")
    bot.register_next_step_handler(msg, process_edit_price_step, car_id, brand, year)

def process_edit_price_step(message, car_id, brand, year):
    price = message.text
    edit_car(car_id, brand, year, price)
    bot.send_message(message.chat.id, "Автомобиль отредактирован!")

# Обработчик команды удаления
def delete_car_command(message):
    msg = bot.send_message(message.chat.id, "Введите ID автомобиля для удаления:")
    bot.register_next_step_handler(msg, process_delete_id_step)

def process_delete_id_step(message):
    car_id = message.text
    delete_car(car_id)
    bot.send_message(message.chat.id, "Автомобиль удален!")

if __name__ == '__main__':
    create_database()  # Создаем базу данных при запуске
    bot.polling(none_stop=True)    