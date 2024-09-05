while True:
    try:
        number = int(input("Введите число: "))
        if number % 2 == 0:
            print("Четное")
        else:
            print("Нечетное")
        break 
    except ValueError:
        print("Ошибка: Введите целое число.") 
