from models.collections import create_collection, find_collection_by_name
from storage import load_collections, insert_collection


def test_insert_and_load(db_conn):
    insert_collection(create_collection("Живопись XIX века", "Полотна"))
    colls = load_collections()
    assert len(colls) == 1
    assert list(colls.values())[0].name == "Живопись XIX века"


def test_unique_name_violation(db_conn):
    import psycopg
    import pytest
    insert_collection(create_collection("Дубликат"))
    with pytest.raises(psycopg.errors.UniqueViolation):
        insert_collection(create_collection("Дубликат"))


def test_find_collection_by_name(db_conn):
    insert_collection(create_collection("Скульптура"))
    colls = load_collections()
    assert find_collection_by_name(colls, "скульптура") is not None
    assert find_collection_by_name(colls, "  Скульптура  ") is not None
    assert find_collection_by_name(colls, "Нет") is None