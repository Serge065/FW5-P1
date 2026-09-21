from exhibits import (
    create_exhibit, add_exhibit, find_exhibits_by_author,
    filter_exhibits_by_condition, sort_exhibits_by_price,
    get_total_price, print_all_exhibits, print_exhibit_info
)
from storage import load_exhibits, save_exhibits
from utils import input_int, input_float, input_str

DATA_FILE = "data/exhibits.json"


def show_menu() -> None:
    print("\n=== Музейный каталог ===")
    print("1. Показать все экспонаты")
    print("2. Добавить экспонат")
    print("3. Найти по автору")
    print("4. Фильтр по состоянию")
    print("5. Сортировка по стоимости")
    print("6. Общая стоимость коллекции")
    print("0. Выход")


def main() -> None:
    exhibits = load_exhibits(DATA_FILE)
    print(f"Загружено экспонатов: {len(exhibits)}")

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_all_exhibits(exhibits)
        elif choice == "2":
            print("--- Добавление нового экспоната ---")
            name = input_str("Название: ")
            author = input_str("Автор: ")
            collection = input_str("Коллекция: ")
            year = input_int("Год создания: ")
            price = input_float("Стоимость: ")
            condition = input_str(
                "Состояние (отличное/хорошее/удовлетворительное): "
            )
            is_available = input_str(
                "Доступен для выставки? (да/нет): "
            ).lower() == "да"
            new_exhibit = create_exhibit(
                name, author, collection, year, price, condition, is_available
            )
            add_exhibit(exhibits, new_exhibit)
            save_exhibits(DATA_FILE, exhibits)
            print("Экспонат добавлен!")
        elif choice == "3":
            query = input_str("Введите имя автора (или часть): ")
            results = find_exhibits_by_author(exhibits, query)
            if results:
                for ex in results:
                    print_exhibit_info(ex)
            else:
                print("Ничего не найдено.")
        elif choice == "4":
            cond = input_str("Введите состояние: ")
            results = filter_exhibits_by_condition(exhibits, cond)
            if results:
                for ex in results:
                    print_exhibit_info(ex)
            else:
                print("Нет экспонатов с таким состоянием.")
        elif choice == "5":
            sorted_ex = sort_exhibits_by_price(exhibits)
            for ex in sorted_ex:
                print_exhibit_info(ex)
        elif choice == "6":
            total = get_total_price(exhibits)
            print(f"Общая стоимость всех экспонатов: {total:.2f} руб.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()