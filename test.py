# Задание 2: Создай функцию, которая возвращает функцию проверки условия
def create_filter_condition(min_value, max_value):
    return lambda x: min_value < x < max_value


# Должно работать так:
age_check = create_filter_condition(18, 65)
score_check = create_filter_condition(90, 100)

ages = [15, 25, 30, 70, 45]
scores = [85, 92, 95, 88, 98]

assert list(filter(age_check, ages)) == [25, 30, 45]
