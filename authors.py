from typing import Any, Dict, List

Author = Dict[str, Any]


def create_author(name: str, lastname: str) -> Author:
    return {
        "id": None,
        "name": name,
        "lastname": lastname
    }
def add_author(authors: Dict[int, Author], author_data: Author) -> int:
    new_id = max(authors.keys(), default=0) + 1
    author_data["id"] = new_id
    authors[new_id] = author_data
    return new_id


def get_author_full_name(author: Author) -> str:
    return f"{author["name"]} {author["lastname"]}"

def find_authors_by_query(authors: Dict[int, Author], query: str) -> List[Author]:
    q = query.lower()
    return [a for a in authors.values() if q in a["name"].lower() or q in a["lastname"].lower()]

def get_author_by_id(authors: Dict[int, Author], author_id: int) -> Author | None:
    return authors.get(author_id)

def print_author_info(author: Author) -> None:
    print(f"--- ID: {author["id"]} ---")
    print(f"Имя: {author["name"]}")
    print(f"Фамилия: {author["lastname"]}\n")
