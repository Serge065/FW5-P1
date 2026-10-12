import os, json
from typing import Dict, List
from models import Author, Collection, Condition, Exhibit
from models.authors import add_author, get_author_by_id
from models.collections import add_collection
from models.conditions import DEFAULT_CONDITIONS, add_condition
from models.exhibits import add_exhibit

def _load_raw_json(filename: str):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except (json.JSONDecodeError, ValueError):
        return {}

def _save_raw_json(filename: str, data: Dict[int, dict]):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_authors(filename: str):
    raw = _load_raw_json(filename)
    authors: Dict[int, Author] = {}
    for key, data in raw.items():
        author = Author.from_data(data)
        authors[author.id] = author
    return authors

def save_authors(filename: str, authors: Dict[int, Author]):
    data = {str(k): v.to_data() for k, v in authors.items()}
    _save_raw_json(filename, data)

def load_collections(filename: str):
    raw = _load_raw_json(filename)
    collections: Dict[int, Collection] = {}
    for key, data in raw.items():
        coll = Collection.from_data(data)
        collections[coll.id] = coll
    return collections

def save_collections(filename: str, collections: Dict[int, Collection]):
    data = {str(k): v.to_data() for k, v in collections.items()}
    _save_raw_json(filename, data)

def load_conditions(filename: str):
    raw = _load_raw_json(filename)
    if not raw:
        return dict(DEFAULT_CONDITIONS)
    conditions: Dict[int, Condition] = {}
    for key, data in raw.items():
        cond = Condition.from_data(data)
        conditions[cond.id] = cond
    return conditions

def save_conditions(filename: str, conditions: Dict[int, Condition]):
    data = {str(k): v.to_data() for k, v in conditions.items()}
    _save_raw_json(filename, data)

def load_exhibits(filename: str, authors: Dict[int, Author], collections: Dict[int, Collection], conditions: Dict[int, Condition]):
    raw = _load_raw_json(filename)
    exhibits: Dict[int, Exhibit] = {}
    for key, data in raw.items():
        exhibit = Exhibit.from_data(data, authors, collections, conditions)
        if exhibit is not None:
            exhibits[exhibit.id] = exhibit
    return exhibits

def save_exhibits(filename: str, exhibits: Dict[int, Exhibit]):
    data = {str(k): v.to_data() for k, v in exhibits.items()}
    _save_raw_json(filename, data)