from datetime import date
from typing import Any, Dict, List
from .authors import Author
from .collections import Collection
from .conditions import Condition

class Exhibit:
    def __init__(self, exhibit_id: int, name: str, author: Author, collection: Collection, condition: Condition, year: int, price: float, is_available: bool):
        self.id = exhibit_id
        self.name = name
        self.author = author
        self.collection = collection
        self.condition = condition
        self.year = year
        self.price = price
        self.is_available = is_available

    def calculate_age(self):
        return date.today().year - self.year

    def get_status(self):
        return self.condition.get_status(self.is_available)

    def __str__(self):
        author_name = (self.author.get_full_name() if self.author else "Неизвестен")
        return (
            f"{self.name} — {author_name}, "
            f"{self.year} г., {self.price} руб."
        )

    @classmethod
    def from_data(cls, data: Dict[str, Any], authors: Dict[int, Author], collections: Dict[int, Collection], conditions: Dict[int, Condition]):
        author = authors.get(data["author_id"])
        collection = collections.get(data["collection_id"])
        condition = conditions.get(data["condition_id"])

        if author is None or collection is None or condition is None:
            return None

        return cls(
            exhibit_id=data["id"],
            name=data["name"],
            author=author,
            collection=collection,
            condition=condition,
            year=data["year"],
            price=data["price"],
            is_available=data["is_available"],
        )

    def to_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "author_id": self.author.id if self.author else None,
            "collection_id": (self.collection.id if self.collection else None),
            "condition_id": (self.condition.id if self.condition else None),
            "year": self.year,
            "price": self.price,
            "is_available": self.is_available,
        }

def create_exhibit(name: str, author: Author, collection: Collection, condition: Condition, year: int, price: float, is_available: bool):
    return Exhibit(
        exhibit_id=0,
        name=name,
        author=author,
        collection=collection,
        condition=condition,
        year=year,
        price=price,
        is_available=is_available,
    )

def add_exhibit(exhibits: Dict[int, Exhibit], exhibit_data: Exhibit):
    new_id = max(exhibits.keys(), default=0) + 1
    exhibit_data.id = new_id
    exhibits[new_id] = exhibit_data
    return new_id


def find_exhibits_by_author(exhibits: Dict[int, Exhibit], authors: Dict[int, Author], query: str):
    q = query.lower()
    matched_ids = {
        aid for aid, a in authors.items()
        if q in a.name.lower() or q in a.lastname.lower()
    }
    return [
        ex for ex in exhibits.values()
        if ex.author and ex.author.id in matched_ids
    ]

def filter_exhibits_by_condition(exhibits: Dict[int, Exhibit], condition_id: int):
    return [ex for ex in exhibits.values() if ex.condition and ex.condition.id == condition_id]

def filter_exhibits_by_collection(exhibits: Dict[int, Exhibit], collection_id: int) -> List[Exhibit]:
    return [ex for ex in exhibits.values() if ex.collection and ex.collection.id == collection_id]

def sort_exhibits_by_price(exhibits: Dict[int, Exhibit]):
    return sorted(exhibits.values(), key=lambda ex: ex.price)

def get_total_price(exhibits: Dict[int, Exhibit]):
    return sum(ex.price for ex in exhibits.values())

def print_exhibit_info(exhibit: Exhibit):
    author_name = (exhibit.author.get_full_name() if exhibit.author else "Неизвестен")
    collection_name = (exhibit.collection.name if exhibit.collection else "Неизвестная коллекция")
    condition_label = (exhibit.condition.label if exhibit.condition else "Неизвестно")
    status = exhibit.get_status()
    age = exhibit.calculate_age()

    print(f"--- ID: {exhibit.id} ---")
    print(f"Название: {exhibit.name}")
    print(f"Автор: {author_name}")
    print(f"Коллекция: {collection_name}")
    print(f"Год создания: {exhibit.year} (возраст: {age} лет)")
    print(f"Стоимость: {exhibit.price} руб.")
    print(f"Состояние: {condition_label}")
    print(f"Доступен: {'да' if exhibit.is_available else 'нет'}")
    print(f"Статус: {status}\n")

def print_all_exhibits(exhibits: Dict[int, Exhibit]):
    if not exhibits:
        print("Список экспонатов пуст.")
        return
    for ex in exhibits.values():
        print_exhibit_info(ex)