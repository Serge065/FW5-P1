from datetime import date
from typing import Any, Dict, List

from authors import Author, get_author_full_name
from collection import Collection, get_collection_name
from conditions import Condition, get_condition_by_id, get_condition_status

Exhibit = Dict[str, Any]


def create_exhibit(
    name: str,
    author_id: int,
    collection_id: int,
    condition_id: int,
    year: int,
    price: float,
    is_available: bool,
) -> Exhibit:
    return {
        "id": None,
        "name": name,
        "author_id": author_id,
        "collection_id": collection_id,
        "condition_id": condition_id,
        "year": year,
        "price": price,
        "is_available": is_available,
    }


def calculate_exhibit_age(year: int) -> int:
    return date.today().year - year


def add_exhibit(exhibits: Dict[int, Exhibit], exhibit_data: Exhibit) -> int:
    new_id = max(exhibits.keys(), default=0) + 1
    exhibit_data["id"] = new_id
    exhibits[new_id] = exhibit_data
    return new_id


def find_exhibits_by_author(
    exhibits: Dict[int, Exhibit],
    authors: Dict[int, Author],
    query: str,
) -> List[Exhibit]:
    q = query.lower()
    matched_ids = {
        aid for aid, a in authors.items()
        if q in a["name"].lower() or q in a["lastname"].lower()
    }
    return [ex for ex in exhibits.values() if ex["author_id"] in matched_ids]


def filter_exhibits_by_condition(
    exhibits: Dict[int, Exhibit], condition_id: int
) -> List[Exhibit]:
    return [
        ex for ex in exhibits.values()
        if ex["condition_id"] == condition_id
    ]


def filter_exhibits_by_collection(
    exhibits: Dict[int, Exhibit], collection_id: int
) -> List[Exhibit]:
    return [
        ex for ex in exhibits.values()
        if ex["collection_id"] == collection_id
    ]


def sort_exhibits_by_price(exhibits: Dict[int, Exhibit]) -> List[Exhibit]:
    return sorted(exhibits.values(), key=lambda ex: ex["price"])


def get_total_price(exhibits: Dict[int, Exhibit]) -> float:
    return sum(ex["price"] for ex in exhibits.values())


def print_exhibit_info(
    exhibit: Exhibit,
    authors: Dict[int, Author],
    collections: Dict[int, Collection],
    conditions: Dict[int, Condition],
) -> None:
    author = authors.get(exhibit["author_id"])
    author_name = get_author_full_name(author) if author else "Неизвестен"
    collection_name = get_collection_name(
        collections, exhibit["collection_id"]
    )
    condition = get_condition_by_id(conditions, exhibit["condition_id"])
    condition_label = condition["label"] if condition else "Неизвестно"
    status = (
        get_condition_status(condition, exhibit["is_available"])
        if condition else "Статус неизвестен"
    )
    age = calculate_exhibit_age(exhibit["year"])

    print(f"--- ID: {exhibit['id']} ---")
    print(f"Название: {exhibit['name']}")
    print(f"Автор: {author_name}")
    print(f"Коллекция: {collection_name}")
    print(f"Год создания: {exhibit['year']} (возраст: {age} лет)")
    print(f"Стоимость: {exhibit['price']} руб.")
    print(f"Состояние: {condition_label}")
    print(f"Доступен: {"да" if exhibit['is_available'] else "нет"}")
    print(f"Статус: {status}")
    print()


def print_all_exhibits(
    exhibits: Dict[int, Exhibit],
    authors: Dict[int, Author],
    collections: Dict[int, Collection],
    conditions: Dict[int, Condition],
) -> None:
    if not exhibits:
        print("Список экспонатов пуст.")
        return
    for ex in exhibits.values():
        print_exhibit_info(ex, authors, collections, conditions)