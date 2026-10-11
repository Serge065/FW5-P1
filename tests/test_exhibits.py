from models.authors import create_author
from models.collections import create_collection
from models.conditions import DEFAULT_CONDITIONS
from models.exhibits import (
    create_exhibit, find_exhibits_by_author,
    filter_exhibits_by_condition, filter_exhibits_by_collection,
    sort_exhibits_by_price, get_total_price,
)
from storage import (
    insert_author, insert_collection, insert_exhibit,
    load_authors, load_collections, load_conditions, load_exhibits,
)


def _seed(db_conn):
    a = create_author("Иван", "Шишкин")
    a.id = insert_author(a)
    c = create_collection("Живопись")
    c.id = insert_collection(c)
    cond = DEFAULT_CONDITIONS[2]
    ex = create_exhibit("Утро в сосновом лесу", a, c, cond, 1889, 3_500_000.0, True)
    ex.id = insert_exhibit(ex)
    return a, c, cond, ex


def test_insert_and_load_exhibit(db_conn):
    a, c, cond, ex = _seed(db_conn)
    authors = load_authors()
    colls = load_collections()
    conds = load_conditions()
    exhibits = load_exhibits(authors, colls, conds)
    assert len(exhibits) == 1
    assert exhibits[ex.id].name == "Утро в сосновом лесу"


def test_price_check_constraint(db_conn):
    import psycopg
    import pytest
    a = create_author("A", "B"); a.id = insert_author(a)
    c = create_collection("C"); c.id = insert_collection(c)
    cond = DEFAULT_CONDITIONS[1]
    bad = create_exhibit("Bad", a, c, cond, 1900, -1.0, True)
    with pytest.raises(psycopg.errors.CheckViolation):
        insert_exhibit(bad)


def test_filter_by_condition(db_conn):
    a, c, cond, ex = _seed(db_conn)
    authors = load_authors()
    colls = load_collections()
    conds = load_conditions()
    exhibits = load_exhibits(authors, colls, conds)
    assert len(filter_exhibits_by_condition(exhibits, cond.id)) == 1
    assert len(filter_exhibits_by_condition(exhibits, 4)) == 0


def test_sort_and_total(db_conn):
    a = create_author("A", "A"); a.id = insert_author(a)
    c = create_collection("C"); c.id = insert_collection(c)
    cond = DEFAULT_CONDITIONS[1]
    for name, price in [("One", 100.0), ("Two", 50.0), ("Three", 300.0)]:
        ex = create_exhibit(name, a, c, cond, 2000, price, True)
        ex.id = insert_exhibit(ex)
    exhibits = load_exhibits(load_authors(), load_collections(), load_conditions())
    sorted_ex = sort_exhibits_by_price(exhibits)
    assert [e.price for e in sorted_ex] == [50.0, 100.0, 300.0]
    assert get_total_price(exhibits) == 450.0