from patients import (add_patient,
                      find_patient,
                      delete_patient,
                      get_all_patients,
                      sort_patients,
                      calculate_age,
                      get_patient_full_name)


def test_add_patient():
    patients = {}
    patient_id = add_patient(
        patients,
        "Иван", "Смирнов",
        "1985-06-15",
        "+79999876543",
        "ivan@mail.ru",
        "POLICY-12345",
        "г. Москва, ул. Ленина, д. 10"
    )

    assert patient_id == 1
    assert len(patients) == 1
    assert patients[1]["first_name"] == "Иван"
    assert patients[1]["last_name"] == "Смирнов"
    assert patients[1]["insurance_policy"] == "POLICY-12345"


def test_find_patient():
    patients = {}

    add_patient(patients, "Иван", "Смирнов", "1985-06-15",
                "+79999876543", "ivan@mail.ru", "POLICY-12345")
    add_patient(patients, "Ольга", "Иванова", "1990-03-22",
                "+79998765432", "olga@mail.ru", "POLICY-67890")

    results = find_patient(patients, "Смирнов")
    assert len(results) == 1
    assert results[0]["last_name"] == "Смирнов"

    results = find_patient(patients, "12345")
    assert len(results) == 1
    assert results[0]["insurance_policy"] == "POLICY-12345"

    results = find_patient(patients, "несуществующий")
    assert len(results) == 0


def test_find_patient_by_policy():
    patients = {}

    add_patient(patients, "Иван", "Смирнов", "1985-06-15",
                "+79999876543", "ivan@mail.ru", "POLICY-12345")
    add_patient(patients, "Ольга", "Иванова", "1990-03-22",
                "+79998765432", "olga@mail.ru", "POLICY-67890")

    results = find_patient(patients, "Смирнов")
    assert len(results) == 1
    assert results[0]["last_name"] == "Смирнов"

    results = find_patient(patients, "12345")
    assert len(results) == 1
    assert results[0]["insurance_policy"] == "POLICY-12345"

    results = find_patient(patients, "несуществующий")
    assert len(results) == 0


def test_delete_patient():
    patients = {}
    patient_id = add_patient(patients, "Иван", "Смирнов", "1985-06-15",
                             "+79999876543", "ivan@mail.ru", "POLICY-12345")

    assert delete_patient(patients, patient_id) is True
    assert len(patients) == 0

    assert delete_patient(patients, 999) is False


def test_get_all_patients():
    patients = {}
    add_patient(patients, "Иван", "Смирнов", "1985-06-15",
                "+79999876543", "ivan@mail.ru", "POLICY-12345")
    add_patient(patients, "Ольга", "Иванова", "1990-03-22",
                "+79998765432", "olga@mail.ru", "POLICY-67890")

    all_patients = get_all_patients(patients)
    assert len(all_patients) == 2


def test_sort_patients():
    patients = {}
    add_patient(patients, "Анна", "Зайцева", "1990-03-22",
                "+79998765432", "anna@mail.ru", "POLICY-111")
    add_patient(patients, "Иван", "Смирнов", "1985-06-15",
                "+79999876543", "ivan@mail.ru", "POLICY-12345")
    add_patient(patients, "Ольга", "Иванова", "1990-03-22",
                "+79998765432", "olga@mail.ru", "POLICY-67890")

    sorted_patients = sort_patients(patients)
    assert sorted_patients[0]["last_name"] == "Зайцева"
    assert sorted_patients[1]["last_name"] == "Иванова"
    assert sorted_patients[2]["last_name"] == "Смирнов"


def test_calculate_age():
    age = calculate_age("1990-03-22")
    assert isinstance(age, int)
    assert age >= 0


def test_get_patient_full_name():
    patient = {
        "first_name": "Иван",
        "last_name": "Смирнов"
    }
    assert get_patient_full_name(patient) == "Смирнов Иван"

    patient = {"first_name": "Иван"}
    assert get_patient_full_name(patient) == "Иван"
