from typing import Any, Dict

Condition = Dict[str, Any]

# Предустановленный справочник состояний.
# code — то, что хранится в JSON экспоната (author_id-подобно)
DEFAULT_CONDITIONS: Dict[int, Condition] = {
    1: {"id": 1, "code": "отличное", "label": "Отличное",
        "needs_restoration": False, "needs_check": False},
    2: {"id": 2, "code": "хорошее", "label": "Хорошее",
        "needs_restoration": False, "needs_check": False},
    3: {"id": 3, "code": "удовлетворительное", "label": "Удовлетворительное",
        "needs_restoration": False, "needs_check": True},
    4: {"id": 4, "code": "плохое", "label": "Плохое",
        "needs_restoration": True, "needs_check": False},
}


def create_condition(
    code: str, label: str,
    needs_restoration: bool = False,
    needs_check: bool = False,
) -> Condition:
    return {
        "id": None,
        "code": code,
        "label": label,
        "needs_restoration": needs_restoration,
        "needs_check": needs_check,
    }


def add_condition(
    conditions: Dict[int, Condition], condition_data: Condition
) -> int:
    new_id = max(conditions.keys(), default=0) + 1
    condition_data["id"] = new_id
    conditions[new_id] = condition_data
    return new_id


def get_condition_by_code(
    conditions: Dict[int, Condition], code: str
) -> Condition | None:
    q = code.lower().strip()
    for c in conditions.values():
        if c["code"].lower() == q:
            return c
    return None


def get_condition_by_id(
    conditions: Dict[int, Condition], condition_id: int
) -> Condition | None:
    return conditions.get(condition_id)


def get_condition_status(
    condition: Condition, is_available: bool
) -> str:
    """Возвращает текстовый статус по состоянию и доступности."""
    if condition["needs_restoration"]:
        return "Экспонат необходимо направить на реставрацию"
    if condition["needs_check"]:
        return "Экспонат требует проверки"
    if not is_available:
        return "Экспонат временно недоступен"
    if condition["code"] == "отличное":
        return "Экспонат готов к выставке"
    return "Экспонат можно выставлять"


def print_condition_info(condition: Condition) -> None:
    print(f"--- ID: {condition['id']} ---")
    print(f"Код: {condition['code']}")
    print(f"Название: {condition['label']}")
    print(f"Требует реставрации: {condition['needs_restoration']}")
    print(f"Требует проверки: {condition['needs_check']}")
    print()