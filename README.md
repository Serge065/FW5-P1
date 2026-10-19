# Музейный каталог

Веб-приложение для учёта экспонатов музея: авторы, коллекции, состояния сохранности и стоимость экспонатов.

Проект развивается поэтапно: консольная версия дополнена веб-интерфейсом на Django и переведена на систему шаблонов Django (ПР6).

---

## 1. Назначение проекта

«Музейный каталог» — учебное приложение, позволяющее:

- хранить сведения об авторах, коллекциях, состояниях сохранности и экспонатах;
- просматривать экспонаты, авторов и коллекции через веб-интерфейс;
- фильтровать и сортировать данные (в консольной версии);
- получать сводную информацию по стоимости.

Проект развивается поэтапно: от консольного приложения на Python и PostgreSQL к веб-приложению на Django с шаблонным слоем представления.

---

## 2. Используемые технологии

- Python 3.12
- Django 5.2
- Django Template Language (DTL)
- HTML5, CSS3, JavaScript
- Bootstrap 5 (CDN)
- PostgreSQL 16 (через `psycopg` и собственный модуль `db.py`)
- Docker / Docker Compose
- pytest, flake8
- Git

---

## 3. Предметная область

Основные сущности:

- **Author** — идентификатор, имя, фамилия;
- **Collection** — идентификатор, название, описание;
- **Condition** — идентификатор, код, название, признаки «требует реставрации» / «требует проверки»;
- **Exhibit** — идентификатор, название, автор, коллекция, состояние, год создания, стоимость, доступность.

Для предметной области реализованы собственные Python-классы в каталоге `models/`.

Данные хранятся в PostgreSQL. Доступ к БД реализован через модуль `db.py` (низкоуровневые запросы `psycopg`) и модуль `storage.py` (функции загрузки/вставки).

> Django ORM и формы Django на текущем этапе не используются. Схема БД создаётся скриптом `schema.sql` при инициализации контейнера PostgreSQL.

---

## 4. Структура проекта

```
museum/
├── authors/
│   ├── templates/authors/
│   │   ├── author_list.html
│   │   ├── author_detail.html
│   │   └── includes/author_card.html
│   ├── urls.py
│   └── views.py
├── colections/                 # Python-пакет (одна «l»)
│   ├── templates/collections/
│   │   ├── collection_list.html
│   │   ├── collection_detail.html
│   │   └── includes/collection_card.html
│   ├── urls.py                 # app_name = "collections"
│   └── views.py
├── exhibits/
│   ├── templates/exhibits/
│   │   ├── exhibit_list.html
│   │   ├── exhibit_detail.html
│   │   └── includes/exhibit_card.html
│   ├── urls.py
│   └── views.py
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── includes/navigation.html
├── models/
│   ├── authors.py
│   ├── collections.py
│   ├── conditions.py
│   └── exhibits.py
├── museum/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tests/
│   ├── conftest.py
│   ├── test_authors.py
│   ├── test_collections.py
│   ├── test_conditions.py
│   └── test_exhibits.py
├── db.py
├── storage.py
├── main.py                     # консольная версия
├── utils.py
├── schema.sql
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## 5. Веб-интерфейс

Веб-часть приложения реализована на Django. Основные страницы:

- `/` — главная;
- `/exhibits/` — список экспонатов;
- `/exhibits/<id>/` — карточка экспоната;
- `/authors/` — список авторов;
- `/authors/<id>/` — карточка автора с перечнем его экспонатов;
- `/collections/` — список коллекций;
- `/collections/<id>/` — карточка коллекции с перечнем экспонатов;
- 404 — собственная страница «не найдено».

Для формирования HTML используется система шаблонов Django. Формирование HTML непосредственно в Python-коде веб-представлений **не используется**: функция `page()` из предыдущей практики удалена.

Представления подготавливают данные и передают их в шаблоны через контекст.

---

## 6. Django Template Language

### 6.1. Базовый шаблон

Общий каркас страниц: `templates/base.html`.

Содержит:

- `<head>`, подключение Bootstrap и собственного CSS;
- подключение навигации через `{% include "includes/navigation.html" %}`;
- блок `{% block title %}` для заголовка вкладки;
- блок `{% block content %}` для содержимого страницы;
- подключение собственного JavaScript.

Дочерние шаблоны используют наследование:

```django
{% extends "base.html" %}

{% block title %}Заголовок страницы{% endblock %}

{% block content %}
    ...
{% endblock %}
```

### 6.2. Включаемые шаблоны

Повторяющиеся фрагменты вынесены в отдельные шаблоны:

- `templates/includes/navigation.html` — общая навигация;
- `exhibits/templates/exhibits/includes/exhibit_card.html` — карточка экспоната;
- `authors/templates/authors/includes/author_card.html` — карточка автора;
- `collections/templates/collections/includes/collection_card.html` — карточка коллекции.

Подключение:

```django
{% include "exhibits/includes/exhibit_card.html" %}
```

### 6.3. Контекст

Представления передают данные в шаблоны через словарь контекста.

Пример для списка экспонатов:

```python
context = {"exhibits": list(exhibits_dict.values())}
return render(request, "exhibits/exhibit_list.html", context)
```

В шаблоне данные доступны по имени переменной:

```django
{% for exhibit in exhibits %}
    ...
{% endfor %}
```

Аналогично передаются `authors`, `collections`, `author`, `collection`, `exhibit`.

### 6.4. Циклы и условия

Циклы:

```django
{% for exhibit in exhibits %}
    ...
{% empty %}
    <p>Экспонаты не найдены.</p>
{% endfor %}
```

Условия используются:

- для проверки наличия объекта (`{% if author %}`, `{% if exhibit %}`, `{% if collection %}`);
- для отображения доступности экспоната;
- для отображения описания коллекции только при его наличии.

Пример:

```django
{% if exhibit.is_available %}
    <span class="badge bg-success">доступен</span>
{% else %}
    <span class="badge bg-danger">недоступен</span>
{% endif %}
```

### 6.5. Фильтры шаблонов

В шаблонах используются стандартные фильтры DTL:

- `{{ exhibits|length }}` — количество элементов;
- `{{ author.get_full_name|default:"Без имени" }}` — значение по умолчанию;
- `{{ collection.description|default:"—" }}` — значение по умолчанию для описания.

Фильтры применяются для представления данных и не содержат бизнес-логики.

### 6.6. Именованные URL и пространства имён

В каждом приложении задано `app_name`, маршруты имеют имена `list` и `detail`.

Ссылки в шаблонах формируются через тег `{% url %}`:

```django
{% url 'homepage:index' %}
{% url 'exhibits:list' %}
{% url 'exhibits:detail' exhibit.id %}
{% url 'authors:list' %}
{% url 'authors:detail' author.id %}
{% url 'collections:list' %}
{% url 'collections:detail' collection.id %}
```

Жёстко заданные адреса в шаблонах не используются.

---

## 7. Статические файлы

Статические файлы приложения `homepage`:

```
homepage/static/homepage/
├── css/style.css
├── js/main.js
└── img/logo.png
```

В `base.html` подключены:

- `{% load static %}` в начале файла;
- CSS: `{% static 'homepage/css/style.css' %}`;
- изображение: `{% static 'homepage/img/logo.png' %}`;
- JavaScript: `{% static 'homepage/js/main.js' %}`.

Собственный CSS оформляет карточки экспонатов, авторов и коллекций, логотип и навигацию. JavaScript используется для отображения текущего года в подвале страницы.

---

## 8. Хранение данных

Данные хранятся в PostgreSQL.

Схема БД и начальные данные (состояния) создаются скриптом `schema.sql` при первичной инициализации контейнера `db`.

Доступ к данным:

- `db.py` — подключение к PostgreSQL (`psycopg`) и функция `execute(...)`;
- `storage.py` — функции загрузки и вставки: `load_authors`, `insert_author`, `load_collections`, `insert_collection`, `load_conditions`, `load_exhibits`, `insert_exhibit`.

Django ORM на текущем этапе не используется, веб-представления работают с предметными объектами через `storage.py`.

---

## 9. Основные модули

- `db.py` — подключение к PostgreSQL, обёртка над `psycopg`.
- `storage.py` — загрузка и сохранение предметных объектов в БД.
- `models/` — классы предметной области: `Author`, `Collection`, `Condition`, `Exhibit`.
- `main.py` — консольный интерфейс (сохранён как предыдущая реализация).
- `utils.py` — вспомогательные функции ввода для консольного интерфейса.
- `exhibits/views.py` — представления экспонатов.
- `authors/views.py` — представления авторов.
- `colections/views.py` — представления коллекций.
- `homepage/views.py` — главная страница и обработчик 404.

---

## 10. Тестирование

Тесты предметной области находятся в каталоге `tests/`:

- `test_authors.py`
- `test_collections.py`
- `test_conditions.py`
- `test_exhibits.py`

Покрывают вставку и загрузку данных, поиск, фильтрацию, сортировку, ограничения БД и вычисление суммарной стоимости.

Запуск:

```bash
pytest -v
```

Тесты используют отдельную тестовую БД `museum_test_db`, которая создаётся и удаляется автоматически (fixtures в `tests/conftest.py`).

---

## 11. Проверка качества кода

```bash
flake8 . --extend-exclude=venv
```

Дополнительно:

```bash
python manage.py check
```

---

## 12. Запуск проекта

### Через Docker Compose

```bash
docker compose up --build
```

Веб-интерфейс: http://localhost:8000/

Проверить логи:

```bash
docker compose logs -f
```

Остановить:

```bash
docker compose down
```

⚠️ Если нужно пересоздать БД с нуля (применится `schema.sql` заново):

```bash
docker compose down -v
docker compose up --build
```

### Локально (без Docker)

1. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate       # Windows
   source .venv/bin/activate    # Linux/macOS
   ```

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Настроить переменные окружения (`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) — в `.env`.

4. Запустить сервер:

   ```bash
   python manage.py runserver
   ```

---


## 13. Текущее состояние проекта (после ПР6)

Реализовано:

- предметные классы `Author`, `Collection`, `Condition`, `Exhibit`;
- хранение данных в PostgreSQL;
- консольный интерфейс (`main.py`);
- Django-проект с приложениями `homepage`, `exhibits`, `authors`, `colections`;
- Django Template Language:
  - базовый шаблон `base.html`;
  - наследование `{% extends %}` и блоки `{% block %}`;
  - включаемые шаблоны `{% include %}`;
  - передача данных через контекст;
  - циклы `{% for %}` и обработка `{% empty %}`;
  - условия `{% if %}`;
  - фильтры `|length`, `|default`;
- именованные URL и пространства имён;
- собственные статические файлы: CSS, JavaScript, изображение;
- собственное оформление карточек и навигации;
- собственная страница 404;
- тесты предметной области (`pytest`);
- проверка стиля кода (`flake8`).

Не реализовано на текущем этапе:

- Django ORM и модели Django;
- формы Django и пользовательский ввод через веб-интерфейс;
- операции создания/редактирования/удаления объектов через веб;
- аутентификация и разграничение доступа.
