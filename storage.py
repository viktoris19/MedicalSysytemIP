import json
from pathlib import Path


def load_data(filename, default=None):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return default if default is not None else {}
    except json.JSONDecodeError:
        print(f'Ошибка: файл {filename} повреждён.')
        return default if default is not None else {}


def save_data(filename, data):
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f'Ошибка при сохранении данных: {e}')
        return False


def load_patients(filename):
    data = load_data(filename, {})
    if data:
        return {int(k): v for k, v in data.items()}
    return {}


def save_patients(filename, patients):
    return save_data(filename, patients)


def load_specialists(filename):
    data = load_data(filename, {})
    if data:
        return {int(k): v for k, v in data.items()}
    return {}


def save_specialists(filename, specialists):
    return save_data(filename, specialists)


def load_appointments(filename):
    data = load_data(filename, {})
    if data:
        return {int(k): v for k, v in data.items()}
    return {}


def save_appointments(filename, appointments):
    return save_data(filename, appointments)


def load_documents(filename):
    data = load_data(filename, {})
    if data:
        return {int(k): v for k, v in data.items()}
    return {}


def save_documents(filename, documents):
    return save_data(filename, documents)
