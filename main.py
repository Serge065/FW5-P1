from datetime import date

exhibit_name = "Зимний пейзаж"
author_name = "Иван Айвазовский"
collection_name = "Живопись XIX века"

creation_year = 1887
price = 2500000.0

condition = "хорошее"
is_available = True


def calculate_exhibit_age(year):
    current_year = date.today().year
    return current_year - year

def get_exhibit_status(condition, is_available):
    if condition == "отличное" and is_available:
        return "Экспонат готов к выставке"
    elif condition == "хорошее" and is_available:
        return "Экспонат можно выставлять"
    elif condition == "удовлетворительное":
        return "Экспонат требует проверки"
    else:
        return "Экспонат необходимо направить на реставрацию"


def print_exhibit_info(
    name,
    author,
    collection,
    year,
    price,
    condition,
    is_available
):
    age = calculate_exhibit_age(year)
    status = get_exhibit_status(condition, is_available)

    print("=== Информация об экспонате ===")
    print(f"Название: {name}")
    print(f"Автор: {author}")
    print(f"Коллекция: {collection}")
    print(f"Год создания: {year}")
    print(f"Возраст: {age} лет")
    print(f"Стоимость: {price} руб.")
    print(f"Состояние: {condition}")
    print(f"Доступен для выставки: {is_available}")
    print(f"Статус: {status}")


print_exhibit_info(
    exhibit_name,
    author_name,
    collection_name,
    creation_year,
    price,
    condition,
    is_available
)