from datetime import date

from models import Patient
from models.patients import (
    add_patient,
    delete_patient,
    find_patient,
    find_patient_by_id,
    get_all_patients,
    sort_patients,
)


def test_patient_creation():
    patient = Patient(
        1, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    assert patient.id == 1
    assert patient.first_name == 'Иван'
    assert patient.last_name == 'Смирнов'
    assert patient.insurance_policy == 'POLICY-12345'


def test_patient_full_name():
    patient = Patient(
        1, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    assert patient.get_full_name() == 'Смирнов Иван'


def test_patient_age():
    patient = Patient(
        1, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    assert patient.get_age() == date.today().year - 1985 - (
        (date.today().month, date.today().day) < (6, 15)
    )


def test_patient_str():
    patient = Patient(
        1, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    text = str(patient)
    assert 'Смирнов Иван' in text
    assert 'POLICY-12345' in text


def test_add_patient():
    patients = []
    patient = add_patient(
        patients, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    assert len(patients) == 1
    assert patient.id == 1
    assert patients[0] is patient


def test_find_patient():
    patients = []
    add_patient(patients, 'Иван', 'Смирнов', '1985-06-15',
                '+79999876543', 'ivan@mail.ru', 'POLICY-12345')
    add_patient(patients, 'Ольга', 'Иванова', '1990-03-22',
                '+79998765432', 'olga@mail.ru', 'POLICY-67890')

    results = find_patient(patients, 'Смирнов')
    assert len(results) == 1
    assert results[0].last_name == 'Смирнов'

    results = find_patient(patients, '12345')
    assert len(results) == 1


def test_find_patient_by_id():
    patients = []
    patient = add_patient(
        patients, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    found = find_patient_by_id(patients, patient.id)
    assert found is patient
    assert find_patient_by_id(patients, 999) is None


def test_delete_patient():
    patients = []
    patient = add_patient(
        patients, 'Иван', 'Смирнов', '1985-06-15',
        '+79999876543', 'ivan@mail.ru', 'POLICY-12345',
    )
    assert delete_patient(patients, patient.id) is True
    assert len(patients) == 0
    assert delete_patient(patients, 999) is False


def test_sort_patients():
    patients = []
    add_patient(patients, 'Анна', 'Зайцева', '1990-03-22',
                '+79998765432', 'anna@mail.ru', 'POLICY-111')
    add_patient(patients, 'Иван', 'Смирнов', '1985-06-15',
                '+79999876543', 'ivan@mail.ru', 'POLICY-12345')

    sorted_list = sort_patients(patients)
    assert sorted_list[0].last_name == 'Зайцева'
    assert sorted_list[1].last_name == 'Смирнов'


def test_get_all_patients():
    patients = []
    add_patient(patients, 'Иван', 'Смирнов', '1985-06-15',
                '+79999876543', 'ivan@mail.ru', 'POLICY-12345')
    assert len(get_all_patients(patients)) == 1