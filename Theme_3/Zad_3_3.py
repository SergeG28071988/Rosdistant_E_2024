class EvenOddChecker:
    def __init__(self):
        self.welcome_message()

    def welcome_message(self):
        print("Добро пожаловать в программу проверки четности числа!")
        print("Введите 'exit' для выхода.")

    def input_number(self):
        while True:
            user_input = input("Введите число: ")
            if user_input.lower() == 'exit':
                print("Выход из программы. До свидания!")
                break
            try:
                number = int(user_input)
                self.check_even_odd(number)
            except ValueError:
                self.handle_error()

    def check_even_odd(self, number):
        if number & 1 == 0:
            print("Четное")
        else:
            print("Нечетное")

    def handle_error(self):
        print("Ошибка: Введите целое число.")

if __name__ == "__main__":
    checker = EvenOddChecker()
    checker.input_number()
