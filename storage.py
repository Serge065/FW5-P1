import json
import os
from typing import Dict


def load_exhibits(filename: str) -> Dict[int, dict]:
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except (json.JSONDecodeError, ValueError):
        print(f"Ошибка: файл {filename} повреждён. Будет создан новый.")
        return {}


def save_exhibits(filename: str, exhibits: Dict[int, dict]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(exhibits, f, ensure_ascii=False, indent=4)
