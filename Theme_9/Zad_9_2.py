from operator import itemgetter

class Car:
    def __init__(self, id, brand, model, year, salon_id):
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.salon_id = salon_id

class Salon:
    def __init__(self, id, salon_name):
        self.id = id
        self.salon_name = salon_name   

class CarSalon:
    def __init__(self, salon_id, car_id):
        self.salon_id = salon_id
        self.car_id = car_id

salons = [
    Salon(1, "Тойота"),
    Salon(2, "Форд"),
    Salon(3, "Шкода"),
    Salon(4, "Субару"),
]

cars = [
    Car(1, "Тойота", "Королла", 2018, 1),
    Car(2, "Тойота", "Camry", 2020, 1),
    Car(3, "Форд", "Фокус", 2019, 2),
    Car(4, "Форд", "Мондео", 2021, 2),
    Car(5, "Шкода", "Октавия", 2018, 3),
    Car(6, "Шкода", "Кодиак", 2020, 3),
    Car(7, "Субару", "Импреза", 2019, 4),
    Car(8, "Субару", "Форестер", 2021, 4),
]

cars_salons = [
    CarSalon(1, 1),  # Автосалон 1 (Тойота) - Автомобиль 1 (Тойота Королла)
    CarSalon(1, 2),  # Автосалон 1 (Тойота) - Автомобиль 2 (Toyota Camry)
    CarSalon(2, 3),  # Автосалон 2 (Форд) - Автомобиль 3 (Форд Фокус)
    CarSalon(2, 4),  # Автосалон 2 (Форд) - Автомобиль 4 (Форд Мондео)
    CarSalon(3, 5),  # Автосалон 3 (Шкода) - Автомобиль 5 (Шкода Октавия)
    CarSalon(3, 6),  # Автосалон 3 (Шкода) - Автомобиль 6 (Шкода Кодиак)
    CarSalon(4, 7),  # Автосалон 4 (Субару) - Автомобиль 7 (Субару Импреза)
    CarSalon(4, 8),  # Автосалон 4 (Субару) - Автомобиль 8 (Субару Форестер)
]
def main():
    one_to_many = []

if __name__ == '__main__':
    main()
