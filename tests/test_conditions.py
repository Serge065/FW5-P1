from models.conditions import get_condition_by_code
from storage import load_conditions


def test_default_conditions_loaded(db_conn):
    conditions = load_conditions()
    assert len(conditions) >= 4
    assert get_condition_by_code(conditions, "хорошее") is not None


def test_condition_status_restoration():
    from models.conditions import Condition
    c = Condition(4, "плохое", "Плохое", needs_restoration=True)
    assert "реставрацию" in c.get_status(is_available=True)


def test_condition_status_check():
    from models.conditions import Condition
    c = Condition(3, "удовлетворительное", "Удовлетворительное", needs_check=True)
    assert "проверки" in c.get_status(is_available=True)


def test_condition_status_unavailable():
    from models.conditions import Condition
    c = Condition(1, "отличное", "Отличное")
    assert "недоступен" in c.get_status(is_available=False)


def test_condition_status_excellent():
    from models.conditions import Condition
    c = Condition(1, "отличное", "Отличное")
    assert "готов" in c.get_status(is_available=True)