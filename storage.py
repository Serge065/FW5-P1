from typing import Dict
from db import execute
from models.authors import Author
from models.collections import Collection
from models.conditions import Condition, DEFAULT_CONDITIONS
from models.exhibits import Exhibit

def load_authors() -> Dict[int, Author]:
    rows = execute("SELECT id, name, lastname FROM authors ORDER BY id", fetch="all")
    return {r["id"]: Author.from_data(r) for r in rows}

def save_authors(authors: Dict[int, Author]) -> None:
    for a in authors.values():
        execute("""
            INSERT INTO authors (id, name, lastname)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, lastname = EXCLUDED.lastname
            """,
            (a.id, a.name, a.lastname),
        )

def insert_author(a: Author) -> int:
    row = execute(
        "INSERT INTO authors (name, lastname) VALUES (%s, %s) RETURNING id",
        (a.name, a.lastname),
        fetch="one",
    )
    return row["id"]

def load_collections() -> Dict[int, Collection]:
    rows = execute(
        "SELECT id, name, description FROM collections ORDER BY id",
        fetch="all",
    )
    return {r["id"]: Collection.from_data(r) for r in rows}

def insert_collection(c: Collection) -> int:
    row = execute(
        "INSERT INTO collections (name, description) VALUES (%s, %s) RETURNING id",
        (c.name, c.description),
        fetch="one",
    )
    return row["id"]

def load_conditions() -> Dict[int, Condition]:
    rows = execute("""
        SELECT id, code, label, needs_restoration, needs_check
        FROM conditions ORDER BY id
        """,
        fetch="all",
    )
    if not rows:
        return dict(DEFAULT_CONDITIONS)
    return {r["id"]: Condition.from_data(r) for r in rows}

def load_exhibits(authors: Dict[int, Author], collections: Dict[int, Collection], conditions: Dict[int, Condition]) -> Dict[int, Exhibit]:
    rows = execute("""
        SELECT id, name, author_id, collection_id, condition_id, year, price, is_available
        FROM exhibits ORDER BY id
        """,
        fetch="all",
    )
    result: Dict[int, Exhibit] = {}
    for r in rows:
        ex = Exhibit.from_data(r, authors, collections, conditions)
        if ex is not None:
            result[ex.id] = ex
    return result


def insert_exhibit(ex: Exhibit) -> int:
    row = execute("""
        INSERT INTO exhibits(name, author_id, collection_id, condition_id, year, price, is_available)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            ex.name,
            ex.author.id,
            ex.collection.id,
            ex.condition.id,
            ex.year,
            ex.price,
            ex.is_available,
        ),
        fetch="one",
    )
    return row["id"]
