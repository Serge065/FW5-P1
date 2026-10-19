from typing import Dict
from models.authors import Author, create_author, find_authors_by_query, print_author_info
from models.collections import Collection, create_collection, find_collection_by_name
from models.conditions import Condition, DEFAULT_CONDITIONS, get_condition_by_code
from models.exhibits import Exhibit, create_exhibit, find_exhibits_by_author, filter_exhibits_by_condition, filter_exhibits_by_collection, sort_exhibits_by_price, get_total_price, print_exhibit_info, print_all_exhibits
from storage import load_authors, load_collections, load_conditions, load_exhibits, insert_author, insert_collection, insert_exhibit
from utils import input_float, input_int, input_str

def pick_author(authors: Dict[int, Author]) -> Author:
    query = input_str("Введите имя/фамилию автора: ")
    found = find_authors_by_query(authors, query)

    if not found:
        print("Автор не найден. Создаём нового.")
        name = input_str("Имя: ")
        lastname = input_str("Фамилия: ")
        author = create_author(name, lastname)
        author.id = insert_author(author)
        authors[author.id] = author
        return author

    if len(found) == 1:
        return found[0]

    for a in found:
        print_author_info(a)
    author_id = input_int("Введите ID автора: ")
    return authors[author_id]

def pick_collection(collections: Dict[int, Collection]) -> Collection:
    name = input_str("Название коллекции: ")
    coll = find_collection_by_name(collections, name)
    if coll:
        return coll

    description = input_str("Описание (можно пусто): ")
    coll = create_collection(name, description)
    coll.id = insert_collection(coll)
    collections[coll.id] = coll
    return coll

def pick_condition(conditions: Dict[int, Condition]) -> Condition:
    code = input_str("Состояние (отличное/хорошее/удовлетворительное/плохое): ")
    cond = get_condition_by_code(conditions, code)
    if not cond:
        print("Неизвестное состояние, используем 'хорошее'.")
        cond = get_condition_by_code(conditions, "хорошее")
    return cond

def show_menu() -> None:
    print("\n=== Музейный каталог ===")
    print("1. Показать все экспонаты")
    print("2. Добавить экспонат")
    print("3. Найти по автору")
    print("4. Фильтр по состоянию")
    print("5. Фильтр по коллекции")
    print("6. Сортировка по стоимости")
    print("7. Общая стоимость коллекции")
    print("0. Выход")


def create_new_exhibit(exhibits: Dict[int, Exhibit], authors: Dict[int, Author], collections: Dict[int, Collection], conditions: Dict[int, Condition]) -> None:
    print("--- Добавление нового экспоната ---")
    name = input_str("Название: ")
    author = pick_author(authors)
    collection = pick_collection(collections)
    condition = pick_condition(conditions)
    year = input_int("Год создания: ")
    price = input_float("Стоимость: ")
    is_available = input_str("Доступен для выставки? (да/нет): ").lower() == "да"

    exhibit = create_exhibit(
        name=name,
        author=author,
        collection=collection,
        condition=condition,
        year=year,
        price=price,
        is_available=is_available,
    )
    exhibit.id = insert_exhibit(exhibit)
    exhibits[exhibit.id] = exhibit
    print("Экспонат добавлен!")

def main() -> None:
    authors     = load_authors()
    collections = load_collections()
    conditions  = load_conditions() or dict(DEFAULT_CONDITIONS)
    exhibits    = load_exhibits(authors, collections, conditions)

    print(f"Загружено экспонатов: {len(exhibits)}")

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_all_exhibits(exhibits)

        elif choice == "2":
            create_new_exhibit(exhibits, authors, collections, conditions)

        elif choice == "3":
            query = input_str("Введите имя автора (или часть): ")
            results = find_exhibits_by_author(exhibits, authors, query)
            for ex in results:
                print_exhibit_info(ex)
            if not results:
                print("Ничего не найдено.")

        elif choice == "4":
            code = input_str("Введите состояние: ")
            cond = get_condition_by_code(conditions, code)
            if not cond:
                print("Нет такого состояния.")
                continue
            results = filter_exhibits_by_condition(exhibits, cond.id)
            for ex in results:
                print_exhibit_info(ex)
            if not results:
                print("Нет экспонатов с таким состоянием.")

        elif choice == "5":
            name = input_str("Название коллекции: ")
            coll = find_collection_by_name(collections, name)
            if not coll:
                print("Коллекция не найдена.")
                continue
            results = filter_exhibits_by_collection(exhibits, coll.id)
            for ex in results:
                print_exhibit_info(ex)
            if not results:
                print("В коллекции нет экспонатов.")

        elif choice == "6":
            for ex in sort_exhibits_by_price(exhibits):
                print_exhibit_info(ex)

        elif choice == "7":
            total = get_total_price(exhibits)
            print(f"Общая стоимость: {total:.2f} руб.")

        elif choice == "0":
            break

        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
