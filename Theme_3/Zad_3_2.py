while True:
    try:
        number = float(input("Введите число: "))
        if number.is_integer():
            if number % 2 == 0:
                print("Четное")
            else:
                print("Нечетное")
            break
        else:
            print("Ошибка: Введите целое число.")
    except ValueError:
        print("Ошибка: Введите число.")
