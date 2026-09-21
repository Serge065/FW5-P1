from datetime import date
from typing import Dict, List

Exhibit = Dict[str, any]


def create_exhibit(
    name: str,
    author: str,
    collection: str,
    year: int,
    price: float,
    condition: str,
    is_available: bool
) -> Exhibit:
    return {
        "id": None,
        "name": name,
        "author": author,
        "collection": collection,
        "year": year,
        "price": price,
        "condition": condition,
        "is_available": is_available
    }


def calculate_exhibit_age(year: int) -> int:
    current_year = date.today().year
    return current_year - year


def get_exhibit_status(condition: str, is_available: bool) -> str:
    if condition == "отличное" and is_available:
        return "Экспонат готов к выставке"
    elif condition == "хорошее" and is_available:
        return "Экспонат можно выставлять"
    elif condition == "удовлетворительное":
        return "Экспонат требует проверки"
    else:
        return "Экспонат необходимо направить на реставрацию"


def add_exhibit(exhibits: Dict[int, Exhibit], exhibit_data: Exhibit) -> int:
    if not exhibits:
        new_id = 1
    else:
        new_id = max(exhibits.keys()) + 1
    exhibit_data["id"] = new_id
    exhibits[new_id] = exhibit_data
    return new_id


def find_exhibits_by_author(
    exhibits: Dict[int, Exhibit], query: str
) -> List[Exhibit]:
    result = []
    for exhibit in exhibits.values():
        if query.lower() in exhibit["author"].lower():
            result.append(exhibit)
    return result


def filter_exhibits_by_condition(
    exhibits: Dict[int, Exhibit], condition: str
) -> List[Exhibit]:
    return [ex for ex in exhibits.values() if ex["condition"] == condition]


def sort_exhibits_by_price(exhibits: Dict[int, Exhibit]) -> List[Exhibit]:
    return sorted(exhibits.values(), key=lambda ex: ex["price"])


def get_total_price(exhibits: Dict[int, Exhibit]) -> float:
    return sum(ex["price"] for ex in exhibits.values())


def print_exhibit_info(exhibit: Exhibit) -> None:
    age = calculate_exhibit_age(exhibit["year"])
    status = get_exhibit_status(exhibit["condition"], exhibit["is_available"])
    print(f"--- ID: {exhibit['id']} ---")
    print(f"Название: {exhibit['name']}")
    print(f"Автор: {exhibit['author']}")
    print(f"Коллекция: {exhibit['collection']}")
    print(f"Год создания: {exhibit['year']} (возраст: {age} лет)")
    print(f"Стоимость: {exhibit['price']} руб.")
    print(f"Состояние: {exhibit['condition']}")
    print(f"Доступен: {exhibit['is_available']}")
    print(f"Статус: {status}")
    print()


def print_all_exhibits(exhibits: Dict[int, Exhibit]) -> None:
    if not exhibits:
        print("Список экспонатов пуст.")
        return
    for exhibit in exhibits.values():
        print_exhibit_info(exhibit)