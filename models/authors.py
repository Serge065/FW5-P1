from typing import Any, Dict

class Author:
    def __init__(self, author_id: int, name: str, lastname: str):
        self.id = author_id
        self.name = name
        self.lastname = lastname

    def get_full_name(self) -> str:
        return f"{self.name} {self.lastname}"

    def __str__(self) -> str:
        return self.get_full_name()

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        return cls(
            author_id=data["id"],
            name=data["name"],
            lastname=data["lastname"],
        )

    def to_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
        }

def add_author(authors: Dict[int, Author], author_data: Author):
    new_id = max(authors.keys(), default=0) + 1
    author_data.id = new_id
    authors[new_id] = author_data
    return new_id

def find_authors_by_query(authors: Dict[int, Author], query: str):
    q = query.lower()
    return [
        a for a in authors.values()
        if q in a.name.lower() or q in a.lastname.lower()
    ]

def get_author_by_id(authors: Dict[int, Author], author_id: int):
    return authors.get(author_id)

def create_author(name: str, lastname: str):
    return Author(author_id=0, name=name, lastname=lastname)

def print_author_info(author: Author) -> None:
    print(f"--- ID: {author.id} ---")
    print(f"Имя: {author.name}")
    print(f"Фамилия: {author.lastname}\n")