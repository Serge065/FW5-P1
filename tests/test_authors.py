from models.authors import Author, create_author, find_authors_by_query
from storage import load_authors, insert_author


def test_insert_author_returns_id(db_conn):
    a = create_author("Иван", "Шишкин")
    new_id = insert_author(a)
    assert isinstance(new_id, int)
    assert new_id > 0


def test_load_authors_after_insert(db_conn):
    insert_author(create_author("Иван", "Шишкин"))
    insert_author(create_author("Огюст", "Роден"))
    authors = load_authors()
    assert len(authors) == 2
    assert any(a.lastname == "Шишкин" for a in authors.values())


def test_find_authors_by_query_case_insensitive(db_conn):
    insert_author(create_author("Иван", "Шишкин"))
    authors = load_authors()
    assert len(find_authors_by_query(authors, "шиш")) == 1
    assert len(find_authors_by_query(authors, "ИВАН")) == 1
    assert len(find_authors_by_query(authors, "неттакого")) == 0


def test_author_full_name():
    a = create_author("Иван", "Шишкин")
    assert a.get_full_name() == "Иван Шишкин"