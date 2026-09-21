from exhibits import (
    create_exhibit, add_exhibit, find_exhibits_by_author,
    filter_exhibits_by_condition, get_total_price
)


def test_create_exhibit():
    ex = create_exhibit(
        "Тест", "Автор", "Коллекция", 2000, 100.0, "хорошее", True
    )
    assert ex["name"] == "Тест"
    assert ex["price"] == 100.0


def test_add_exhibit():
    exhibits = {}
    ex = create_exhibit(
        "Картина", "Репин", "Живопись", 1880, 500000.0, "отличное", True
    )
    new_id = add_exhibit(exhibits, ex)
    assert len(exhibits) == 1
    assert new_id == 1
    assert exhibits[1]["name"] == "Картина"


def test_find_exhibits_by_author():
    exhibits = {}
    add_exhibit(
        exhibits,
        create_exhibit("А", "Иван Айвазовский", "К", 1900, 100, "хорошее", True)
    )
    add_exhibit(
        exhibits,
        create_exhibit("Б", "Илья Репин", "К", 1900, 100, "хорошее", True)
    )
    results = find_exhibits_by_author(exhibits, "айваз")
    assert len(results) == 1
    assert results[0]["author"] == "Иван Айвазовский"


def test_filter_exhibits_by_condition():
    exhibits = {}
    add_exhibit(
        exhibits,
        create_exhibit("А", "Автор", "К", 1900, 100, "отличное", True)
    )
    add_exhibit(
        exhibits,
        create_exhibit("Б", "Автор", "К", 1900, 100, "хорошее", True)
    )
    results = filter_exhibits_by_condition(exhibits, "отличное")
    assert len(results) == 1


def test_get_total_price():
    exhibits = {}
    add_exhibit(
        exhibits,
        create_exhibit("А", "Автор", "К", 1900, 100.0, "хорошее", True)
    )
    add_exhibit(
        exhibits,
        create_exhibit("Б", "Автор", "К", 1900, 200.0, "хорошее", True)
    )
    assert get_total_price(exhibits) == 300.0
