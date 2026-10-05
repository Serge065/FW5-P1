from models import Author
from models.authors import add_author, find_authors_by_query, get_author_by_id
from models import Collection
from models.collections import add_collection, find_collection_by_name, get_collection_name
from models import Condition
from models.conditions import DEFAULT_CONDITIONS, add_condition, get_condition_by_code, get_condition_by_id
from models import Author, Collection, Condition, Exhibit
from models.exhibits import add_exhibit, create_exhibit, filter_exhibits_by_collection, filter_exhibits_by_condition, find_exhibits_by_author, get_total_price, sort_exhibits_by_price

def test_author_creation():
    author = Author(1, "Иван", "Айвазовский")
    assert author.id == 1
    assert author.name == "Иван"
    assert author.lastname == "Айвазовский"

def test_author_full_name():
    author = Author(1, "Иван", "Айвазовский")
    assert author.get_full_name() == "Иван Айвазовский"

def test_author_str():
    author = Author(1, "Иван", "Айвазовский")
    assert str(author) == "Иван Айвазовский"

def test_author_from_data():
    data = {"id": 1, "name": "Иван", "lastname": "Айвазовский"}
    author = Author.from_data(data)
    assert author.id == 1
    assert author.name == "Иван"
    assert author.lastname == "Айвазовский"

def test_add_author():
    authors = {}
    author = Author(0, "Иван", "Айвазовский")
    new_id = add_author(authors, author)
    assert new_id == 1
    assert authors[1] is author
    assert author.id == 1

def test_find_authors_by_query():
    authors = {
        1: Author(1, "Иван", "Айвазовский"),
        2: Author(2, "Пётр", "Петров"),
    }
    result = find_authors_by_query(authors, "Иван")
    assert len(result) == 1
    assert result[0].id == 1

def test_get_author_by_id():
    authors = {1: Author(1, "Иван", "Айвазовский")}
    author = get_author_by_id(authors, 1)
    assert author is not None
    assert author.id == 1
    assert get_author_by_id(authors, 999) is None
    
def test_collection_creation():
    coll = Collection(1, "Живопись XIX века", "Описание")
    assert coll.id == 1
    assert coll.name == "Живопись XIX века"
    assert coll.description == "Описание"

def test_collection_str():
    coll = Collection(1, "Живопись", "Описание")
    assert str(coll) == "Живопись (Описание)"
    coll2 = Collection(2, "Скульптура")
    assert str(coll2) == "Скульптура"

def test_collection_from_data():
    data = {"id": 1, "name": "Живопись", "description": "Описание"}
    coll = Collection.from_data(data)
    assert coll.id == 1
    assert coll.name == "Живопись"
    assert coll.description == "Описание"

def test_add_collection():
    collections = {}
    coll = Collection(0, "Живопись")
    new_id = add_collection(collections, coll)
    assert new_id == 1
    assert collections[1] is coll

def test_find_collection_by_name():
    collections = {
        1: Collection(1, "Живопись XIX века"),
        2: Collection(2, "Скульптура"),
    }
    result = find_collection_by_name(collections, "живопись xix века")
    assert result is not None
    assert result.id == 1
    assert find_collection_by_name(collections, "неизвестно") is None

def test_get_collection_name():
    collections = {1: Collection(1, "Живопись")}
    assert get_collection_name(collections, 1) == "Живопись"
    assert get_collection_name(collections, 999) == "Неизвестная коллекция"
    
def test_condition_creation():
    cond = Condition(1, "отличное", "Отличное", False, False)
    assert cond.id == 1
    assert cond.code == "отличное"
    assert cond.label == "Отличное"
    assert cond.needs_restoration is False
    assert cond.needs_check is False

def test_condition_str():
    cond = Condition(1, "отличное", "Отличное")
    assert str(cond) == "Отличное"

def test_condition_from_data():
    data = {
        "id": 1,
        "code": "отличное",
        "label": "Отличное",
        "needs_restoration": False,
        "needs_check": False,
    }
    cond = Condition.from_data(data)
    assert cond.id == 1
    assert cond.code == "отличное"
    assert cond.label == "Отличное"
    assert cond.needs_restoration is False
    assert cond.needs_check is False

def test_condition_to_data():
    cond = Condition(1, "отличное", "Отличное", False, False)
    data = cond.to_data()
    assert data == {
        "id": 1,
        "code": "отличное",
        "label": "Отличное",
        "needs_restoration": False,
        "needs_check": False,
    }

def test_condition_status_ready():
    cond = Condition(1, "отличное", "Отличное", False, False)
    assert cond.get_status(True) == "Экспонат готов к выставке"

def test_condition_status_available():
    cond = Condition(2, "хорошее", "Хорошее", False, False)
    assert cond.get_status(True) == "Экспонат можно выставлять"

def test_condition_status_unavailable():
    cond = Condition(1, "отличное", "Отличное", False, False)
    assert cond.get_status(False) == "Экспонат временно недоступен"

def test_condition_status_restoration():
    cond = Condition(4, "плохое", "Плохое", True, False)
    assert cond.get_status(True) == ("Экспонат необходимо направить на реставрацию")

def test_condition_status_check():
    cond = Condition(3, "удовл", "Удовлетворительное", False, True)
    assert cond.get_status(True) == "Экспонат требует проверки"

def test_add_condition():
    conditions = {}
    cond = Condition(0, "новое", "Новое")
    new_id = add_condition(conditions, cond)
    assert new_id == 1
    assert conditions[1] is cond
    assert cond.id == 1

def test_get_condition_by_code():
    conditions = {1: Condition(1, "отличное", "Отличное"), 2: Condition(2, "хорошее", "Хорошее")}
    result = get_condition_by_code(conditions, "ОТЛИЧНОЕ")
    assert result is not None
    assert result.id == 1
    assert get_condition_by_code(conditions, "неизвестно") is None

def test_get_condition_by_id():
    conditions = {1: Condition(1, "отличное", "Отличное")}
    assert get_condition_by_id(conditions, 1) is not None
    assert get_condition_by_id(conditions, 999) is None

def test_default_conditions():
    assert len(DEFAULT_CONDITIONS) == 4
    assert DEFAULT_CONDITIONS[1].code == "отличное"
    assert DEFAULT_CONDITIONS[4].needs_restoration is True
    assert DEFAULT_CONDITIONS[3].needs_check is True

def make_author(author_id=1, name="Иван", lastname="Айвазовский"):
    return Author(author_id, name, lastname)

def make_collection(coll_id=1, name="Живопись"):
    return Collection(coll_id, name)

def make_condition(cond_id=1, code="отличное", label="Отличное"):
    return Condition(cond_id, code, label)

def make_exhibit(exhibit_id=1, name="Зимний пейзаж", author=None, collection=None, condition=None, year=1887, price=2500000.0, is_available=True):
    return Exhibit(
        exhibit_id=exhibit_id,
        name=name,
        author=author or make_author(),
        collection=collection or make_collection(),
        condition=condition or make_condition(),
        year=year,
        price=price,
        is_available=is_available,
    )

def test_exhibit_creation():
    author = make_author()
    collection = make_collection()
    condition = make_condition()
    ex = Exhibit(1, "Зимний пейзаж", author, collection, condition, 1887, 2500000.0, True)
    assert ex.id == 1
    assert ex.name == "Зимний пейзаж"
    assert ex.author is author
    assert ex.collection is collection
    assert ex.condition is condition
    assert ex.year == 1887
    assert ex.price == 2500000.0
    assert ex.is_available is True

def test_exhibit_calculate_age():
    ex = make_exhibit(year=2000)
    from datetime import date
    expected = date.today().year - 2000
    assert ex.calculate_age() == expected

def test_exhibit_get_status():
    cond = make_condition(code="отличное", label="Отличное")
    ex = make_exhibit(condition=cond, is_available=True)
    assert ex.get_status() == "Экспонат готов к выставке"

def test_exhibit_str():
    author = make_author(name="Иван", lastname="Айвазовский")
    ex = make_exhibit(name="Зимний пейзаж", author=author, year=1887, price=1000.0)
    assert str(ex) == ("Зимний пейзаж — Иван Айвазовский, 1887 г., 1000.0 руб.")

def test_exhibit_to_data():
    author = make_author(author_id=1)
    collection = make_collection(coll_id=2)
    condition = make_condition(cond_id=3)
    ex = make_exhibit(exhibit_id=5, author=author, collection=collection, condition=condition, year=1887, price=1000.0, is_available=True)
    data = ex.to_data()
    assert data == {
        "id": 5,
        "name": "Зимний пейзаж",
        "author_id": 1,
        "collection_id": 2,
        "condition_id": 3,
        "year": 1887,
        "price": 1000.0,
        "is_available": True,
    }

def test_exhibit_from_data():
    authors = {1: make_author(author_id=1)}
    collections = {1: make_collection(coll_id=1)}
    conditions = {1: make_condition(cond_id=1)}
    data = {
        "id": 1,
        "name": "Зимний пейзаж",
        "author_id": 1,
        "collection_id": 1,
        "condition_id": 1,
        "year": 1887,
        "price": 1000.0,
        "is_available": True,
    }
    ex = Exhibit.from_data(data, authors, collections, conditions)
    assert ex is not None
    assert ex.id == 1
    assert ex.author is authors[1]
    assert ex.collection is collections[1]
    assert ex.condition is conditions[1]

def test_exhibit_from_data_missing_author():
    authors = {}
    collections = {1: make_collection(coll_id=1)}
    conditions = {1: make_condition(cond_id=1)}
    data = {
        "id": 1,
        "name": "Зимний пейзаж",
        "author_id": 1,
        "collection_id": 1,
        "condition_id": 1,
        "year": 1887,
        "price": 1000.0,
        "is_available": True,
    }
    ex = Exhibit.from_data(data, authors, collections, conditions)
    assert ex is None

def test_exhibit_from_data_missing_collection():
    authors = {1: make_author(author_id=1)}
    collections = {}
    conditions = {1: make_condition(cond_id=1)}
    data = {
        "id": 1,
        "name": "Зимний пейзаж",
        "author_id": 1,
        "collection_id": 1,
        "condition_id": 1,
        "year": 1887,
        "price": 1000.0,
        "is_available": True,
    }
    ex = Exhibit.from_data(data, authors, collections, conditions)
    assert ex is None

def test_create_exhibit():
    author = make_author()
    collection = make_collection()
    condition = make_condition()
    ex = create_exhibit("Новый", author, collection, condition, 2000, 500.0, True)
    assert ex.name == "Новый"
    assert ex.author is author
    assert ex.collection is collection
    assert ex.condition is condition
    assert ex.year == 2000
    assert ex.price == 500.0
    assert ex.is_available is True

def test_add_exhibit():
    exhibits = {}
    ex = make_exhibit()
    new_id = add_exhibit(exhibits, ex)
    assert new_id == 1
    assert exhibits[1] is ex
    assert ex.id == 1

def test_find_exhibits_by_author():
    author1 = make_author(1, "Иван", "Айвазовский")
    author2 = make_author(2, "Пётр", "Петров")
    authors = {1: author1, 2: author2}
    exhibits = {1: make_exhibit(exhibit_id=1, author=author1), 2: make_exhibit(exhibit_id=2, author=author2)}
    result = find_exhibits_by_author(exhibits, authors, "Айвазовский")
    assert len(result) == 1
    assert result[0].id == 1
    result2 = find_exhibits_by_author(exhibits, authors, "Пётр")
    assert len(result2) == 1
    assert result2[0].id == 2
    result3 = find_exhibits_by_author(exhibits, authors, "Неизвестный")
    assert result3 == []

def test_filter_exhibits_by_condition():
    cond1 = make_condition(1, "отличное", "Отличное")
    cond2 = make_condition(2, "хорошее", "Хорошее")
    exhibits = {1: make_exhibit(exhibit_id=1, condition=cond1), 2: make_exhibit(exhibit_id=2, condition=cond2),}
    result = filter_exhibits_by_condition(exhibits, 1)
    assert len(result) == 1
    assert result[0].id == 1
    assert filter_exhibits_by_condition(exhibits, 999) == []

def test_filter_exhibits_by_collection():
    coll1 = make_collection(1, "Живопись")
    coll2 = make_collection(2, "Скульптура")
    exhibits = {1: make_exhibit(exhibit_id=1, collection=coll1), 2: make_exhibit(exhibit_id=2, collection=coll2)}
    result = filter_exhibits_by_collection(exhibits, 2)
    assert len(result) == 1
    assert result[0].id == 2
    assert filter_exhibits_by_collection(exhibits, 999) == []

def test_sort_exhibits_by_price():
    exhibits = {
        1: make_exhibit(exhibit_id=1, price=300.0),
        2: make_exhibit(exhibit_id=2, price=100.0),
        3: make_exhibit(exhibit_id=3, price=200.0),
    }
    result = sort_exhibits_by_price(exhibits)
    assert [ex.price for ex in result] == [100.0, 200.0, 300.0]

def test_get_total_price():
    exhibits = {
        1: make_exhibit(exhibit_id=1, price=100.0),
        2: make_exhibit(exhibit_id=2, price=200.0),
        3: make_exhibit(exhibit_id=3, price=300.0),
    }
    assert get_total_price(exhibits) == 600.0

def test_get_total_price_empty():
    assert get_total_price({}) == 0