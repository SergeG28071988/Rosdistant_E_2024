def main_menu():
    print("Добро пожаловать в программу определения четности числа!")
    print("1. Ввести число")
    print("2. Выход")

def check_even_odd(number):
    if number.is_integer():
        if number % 2 == 0:
            return "Четное"
        else:
            return "Нечетное"
    else:
        return "Ошибка: Введите целое число."

def get_number():
    while True:
        try:
            user_input = input("Введите число: ")
            number = float(user_input)
            return number
        except ValueError:
            print("Ошибка: Введите корректное число. Например, 5 или 3.14.")

def main():
    while True:
        main_menu()
        choice = input("Выберите действие (1 или 2): ")
        
        if choice == '1':
            number = get_number()
            result = check_even_odd(number)
            print(result)
        elif choice == '2':
            print("Спасибо за использование программы! До свидания!")
            break
        else:
            print("Ошибка: Пожалуйста, выберите 1 или 2.")

if __name__ == "__main__":
    main()
