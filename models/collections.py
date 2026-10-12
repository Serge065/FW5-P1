from typing import Any, Dict

class Collection:
    def __init__(self, collection_id: int, name: str, description: str = ""):
        self.id = collection_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        if self.description:
            return f"{self.name} ({self.description})"
        return self.name

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        return cls(
            collection_id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
        )

    def to_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

def add_collection(collections: Dict[int, Collection], collection_data: Collection):
    new_id = max(collections.keys(), default=0) + 1
    collection_data.id = new_id
    collections[new_id] = collection_data
    return new_id

def create_collection(name: str, description: str = ""):
    return Collection(
        collection_id=0,
        name=name,
        description=description,
    )

def get_collection_name(collections: Dict[int, Collection], collection_id: int):
    coll = collections.get(collection_id)
    return coll.name if coll else "Неизвестная коллекция"


def find_collection_by_name(collections: Dict[int, Collection], name: str) :
    q = name.lower().strip()
    for c in collections.values():
        if c.name.lower() == q:
            return c
    return None

def print_collection_info(collection: Collection):
    print(f"--- ID: {collection.id} ---")
    print(f"Название: {collection.name}")
    if collection.description:
        print(f"Описание: {collection.description}")
    print()