from typing import Any, Dict, Optional

class Condition:
    def __init__(self,condition_id: int,code: str,label: str,needs_restoration: bool = False,needs_check: bool = False,) -> None:
        self.id = condition_id
        self.code = code
        self.label = label
        self.needs_restoration = needs_restoration
        self.needs_check = needs_check

    def get_status(self, is_available: bool):
        if self.needs_restoration:
            return "Экспонат необходимо направить на реставрацию"
        if self.needs_check:
            return "Экспонат требует проверки"
        if not is_available:
            return "Экспонат временно недоступен"
        if self.code == "отличное":
            return "Экспонат готов к выставке"
        return "Экспонат можно выставлять"

    def __str__(self):
        return self.label

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        return cls(
            condition_id=data["id"],
            code=data["code"],
            label=data["label"],
            needs_restoration=data.get("needs_restoration", False),
            needs_check=data.get("needs_check", False),
        )

    def to_data(self):
        return {
            "id": self.id,
            "code": self.code,
            "label": self.label,
            "needs_restoration": self.needs_restoration,
            "needs_check": self.needs_check,
        }

DEFAULT_CONDITIONS = {
    1: Condition(1, "отличное", "Отличное", False, False),
    2: Condition(2, "хорошее", "Хорошее", False, False),
    3: Condition(3, "удовлетворительное", "Удовлетворительное", False, True),
    4: Condition(4, "плохое", "Плохое", True, False),
}

def create_condition(code: str,label: str,needs_restoration: bool = False,needs_check: bool = False,):
    return Condition(
        condition_id=0,
        code=code,
        label=label,
        needs_restoration=needs_restoration,
        needs_check=needs_check,
    )
    
def add_condition(conditions: Dict[int, Condition], condition_data: Condition):
    new_id = max(conditions.keys(), default=0) + 1
    condition_data.id = new_id
    conditions[new_id] = condition_data
    return new_id

def get_condition_by_code(conditions: Dict[int, Condition], code: str):
    q = code.lower().strip()
    for c in conditions.values():
        if c.code.lower() == q:
            return c
    return None
def get_condition_by_id(conditions: Dict[int, Condition], condition_id: int):
    return conditions.get(condition_id)

def print_condition_info(condition: Condition):
    print(f"--- ID: {condition.id} ---")
    print(f"Код: {condition.code}")
    print(f"Название: {condition.label}")
    print(f"Требует реставрации: {condition.needs_restoration}")
    print(f"Требует проверки: {condition.needs_check}\n")