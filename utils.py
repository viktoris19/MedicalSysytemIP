from datetime import datetime, date
from typing import Optional


def input_int(
        prompt: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Ошибка: значение должно быть не меньше {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Ошибка: значение должно быть не больше {max_val}")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число")


def input_date(prompt: str) -> Optional[date]:
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                return None
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")


def input_str(prompt: str, required: bool = True) -> Optional[str]:
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("Ошибка: поле обязательно для заполнения")
            continue
        return value if value else None


def input_choice(prompt: str, options: list) -> str:
    while True:
        value = input(prompt).strip().lower()
        if value in [str(opt).lower() for opt in options]:
            return value
        print(f"Ошибка: выберите из вариантов: {', '.join(map(str, options))}")
