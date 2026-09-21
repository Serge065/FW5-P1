def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")

def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")

def input_str(prompt: str) -> str:
    return input(prompt).strip()