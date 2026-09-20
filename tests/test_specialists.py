from models import Specialist
from models.specialists import (
    add_specialist,
    delete_specialist,
    find_specialist,
    get_specialist_by_id,
    sort_specialists,
)


def test_specialist_creation():
    specialist = Specialist(
        1, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert specialist.id == 1
    assert specialist.speciality == 'Кардиолог'
    assert specialist.experience_years == 15


def test_specialist_full_name():
    specialist = Specialist(
        1, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert specialist.get_full_name() == 'Петрова Анна'


def test_specialist_is_experienced():
    specialist = Specialist(
        1, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert specialist.is_experienced() is True

    junior = Specialist(
        2, 'Пётр', 'Сидоров', 'Терапевт',
        '+79990000000', 'sidorov@clinic.ru', 2,
    )
    assert junior.is_experienced() is False


def test_specialist_str():
    specialist = Specialist(
        1, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert 'Петрова Анна' in str(specialist)
    assert 'Кардиолог' in str(specialist)


def test_add_specialist():
    specialists = []
    specialist = add_specialist(
        specialists, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert len(specialists) == 1
    assert specialist.id == 1


def test_find_specialist():
    specialists = []
    add_specialist(specialists, 'Анна', 'Петрова', 'Кардиолог',
                   '+79991234567', 'petrova@clinic.ru', 15)
    add_specialist(specialists, 'Михаил', 'Соколов', 'Терапевт',
                   '+79992345678', 'sokolov@clinic.ru', 8)

    assert len(find_specialist(specialists, 'Петрова')) == 1
    assert len(find_specialist(specialists, 'кардиолог')) == 1
    assert len(find_specialist(specialists, 'нет')) == 0


def test_get_specialist_by_id():
    specialists = []
    specialist = add_specialist(
        specialists, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert get_specialist_by_id(specialists, specialist.id) is specialist
    assert get_specialist_by_id(specialists, 999) is None


def test_delete_specialist():
    specialists = []
    specialist = add_specialist(
        specialists, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 15,
    )
    assert delete_specialist(specialists, specialist.id) is True
    assert len(specialists) == 0
    assert delete_specialist(specialists, 999) is False


def test_sort_specialists():
    specialists = []
    add_specialist(specialists, 'Анна', 'Зайцева', 'Невролог',
                   '+79991111111', 'z@clinic.ru', 5)
    add_specialist(specialists, 'Михаил', 'Соколов', 'Терапевт',
                   '+79992345678', 's@clinic.ru', 8)

    sorted_list = sort_specialists(specialists)
    assert sorted_list[0].last_name == 'Зайцева'
    assert sorted_list[1].last_name == 'Соколов'