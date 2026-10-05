from typing import Any, Dict, List

Collection = Dict[str, Any]


def create_collection(name: str, description: str = "") -> Collection:
    return {
        "id": None,
        "name": name,
        "description": description,
    }


def add_collection(
    collections: Dict[int, Collection], collection_data: Collection
) -> int:
    new_id = max(collections.keys(), default=0) + 1
    collection_data["id"] = new_id
    collections[new_id] = collection_data
    return new_id


def get_collection_name(
    collections: Dict[int, Collection], collection_id: int
) -> str:
    coll = collections.get(collection_id)
    return coll["name"] if coll else "Неизвестная коллекция"


def find_collection_by_name(
    collections: Dict[int, Collection], name: str
) -> Collection | None:
    q = name.lower().strip()
    for c in collections.values():
        if c["name"].lower() == q:
            return c
    return None


def print_collection_info(collection: Collection) -> None:
    print(f"--- ID: {collection['id']} ---")
    print(f"Название: {collection['name']}")
    if collection.get("description"):
        print(f"Описание: {collection['description']}")
    print()