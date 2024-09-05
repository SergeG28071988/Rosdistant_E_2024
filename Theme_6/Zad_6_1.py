import random

# Создаем словарь с случайными элементами
my_dict = {}
for i in range(10):
    key = f"Ключ {i}"
    value = random.randint(1, 100)
    my_dict[key] = value

# Сортируем словарь по значениям
sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))

# Выводим отсортированный словарь
print(sorted_dict) 
