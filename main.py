from authors import (
    add_author, create_author, find_authors_by_query, print_author_info
)
from collection import (
    add_collection, create_collection, find_collection_by_name,
    print_collection_info
)
from conditions import DEFAULT_CONDITIONS, get_condition_by_code
from exhibits import (
    add_exhibit, create_exhibit, filter_exhibits_by_collection,
    filter_exhibits_by_condition, get_total_price, print_all_exhibits,
    print_exhibit_info, sort_exhibits_by_price,
)
from storage import load_json, save_json
from utils import input_float, input_int, input_str

AUTHORS_FILE = "data/authors.json"
COLLECTIONS_FILE = "data/collections.json"
CONDITIONS_FILE = "data/conditions.json"
EXHIBITS_FILE = "data/exhibits.json"


def load_all():
    authors = load_json(AUTHORS_FILE)
    collections = load_json(COLLECTIONS_FILE)
    conditions = load_json(CONDITIONS_FILE) or DEFAULT_CONDITIONS
    exhibits = load_json(EXHIBITS_FILE)
    return authors, collections, conditions, exhibits


def pick_author(authors):
    query = input_str("Введите имя/фамилию автора: ")
    found = find_authors_by_query(authors, query)
    if not found:
        print("Автор не найден. Создаём нового.")
        name = input_str("Имя: ")
        lastname = input_str("Фамилия: ")
        author = create_author(name, lastname)
        add_author(authors, author)
        save_json(AUTHORS_FILE, authors)
        return author["id"]
    if len(found) == 1:
        return found[0]["id"]
    for a in found:
        print_author_info(a)
    return input_int("Введите ID автора: ")


def pick_collection(collections):
    name = input_str("Название коллекции: ")
    coll = find_collection_by_name(collections, name)
    if coll:
        return coll["id"]
    description = input_str("Описание (можно пусто): ")
    coll = create_collection(name, description)
    add_collection(collections, coll)
    save_json(COLLECTIONS_FILE, collections)
    return coll["id"]


def pick_condition(conditions):
    code = input_str(
        "Состояние (отличное/хорошее/удовлетворительное/плохое): "
    )
    cond = get_condition_by_code(conditions, code)
    if not cond:
        print("Неизвестное состояние, используем 'хорошее'.")
        cond = get_condition_by_code(conditions, "хорошее")
    return cond["id"]


def show_menu():
    print("\n=== Музейный каталог ===")
    print("1. Показать все экспонаты")
    print("2. Добавить экспонат")
    print("3. Найти по автору")
    print("4. Фильтр по состоянию")
    print("5. Фильтр по коллекции")
    print("6. Сортировка по стоимости")
    print("7. Общая стоимость коллекции")
    print("0. Выход")


def main():
    authors, collections, conditions, exhibits = load_all()
    print(f"Загружено экспонатов: {len(exhibits)}")

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_all_exhibits(exhibits, authors, collections, conditions)
        elif choice == "2":
            print("--- Добавление нового экспоната ---")
            name = input_str("Название: ")
            author_id = pick_author(authors)
            collection_id = pick_collection(collections)
            condition_id = pick_condition(conditions)
            year = input_int("Год создания: ")
            price = input_float("Стоимость: ")
            is_available = input_str(
                "Доступен для выставки? (да/нет): "
            ).lower() == "да"
            ex = create_exhibit(
                name, author_id, collection_id, condition_id,
                year, price, is_available,
            )
            add_exhibit(exhibits, ex)
            save_json(EXHIBITS_FILE, exhibits)
            print("Экспонат добавлен!")
        elif choice == "3":
            query = input_str("Введите имя автора (или часть): ")
            results = find_exhibits_by_author(exhibits, authors, query)
            for ex in results:
                print_exhibit_info(ex, authors, collections, conditions)
            if not results:
                print("Ничего не найдено.")
        elif choice == "4":
            code = input_str("Введите состояние: ")
            cond = get_condition_by_code(conditions, code)
            if not cond:
                print("Нет такого состояния.")
                continue
            results = filter_exhibits_by_condition(exhibits, cond["id"])
            for ex in results:
                print_exhibit_info(ex, authors, collections, conditions)
            if not results:
                print("Нет экспонатов с таким состоянием.")
        elif choice == "5":
            name = input_str("Название коллекции: ")
            coll = find_collection_by_name(collections, name)
            if not coll:
                print("Коллекция не найдена.")
                continue
            results = filter_exhibits_by_collection(exhibits, coll["id"])
            for ex in results:
                print_exhibit_info(ex, authors, collections, conditions)
            if not results:
                print("В коллекции нет экспонатов.")
        elif choice == "6":
            for ex in sort_exhibits_by_price(exhibits):
                print_exhibit_info(ex, authors, collections, conditions)
        elif choice == "7":
            total = get_total_price(exhibits)
            print(f"Общая стоимость: {total:.2f} руб.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    main()