import os
from typing import List

from models import Appointment, Document, Patient, Specialist
from models.appointments import (
    create_appointment
)
from models.documents import (
    add_document
)
from models.patients import (
    find_patient_by_id,
    sort_patients
)
from models.specialists import (
    get_specialist_by_id,
    sort_specialists
)
import storage
import utils

DATA_DIR = 'data'
PATIENTS_FILE = os.path.join(DATA_DIR, 'patients.json')
SPECIALISTS_FILE = os.path.join(DATA_DIR, 'specialists.json')
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.json')
DOCUMENTS_FILE = os.path.join(DATA_DIR, 'documents.json')

patients: List[Patient] = []
specialists: List[Specialist] = []
appointments: List[Appointment] = []
documents: List[Document] = []


def load_all_data() -> None:
    global patients, specialists, appointments, documents
    patients = storage.load_patients(PATIENTS_FILE)
    specialists = storage.load_specialists(SPECIALISTS_FILE)
    appointments = storage.load_appointments(
        APPOINTMENTS_FILE, patients, specialists,
    )
    documents = storage.load_documents(DOCUMENTS_FILE, appointments)


def save_all_data() -> None:
    storage.save_patients(PATIENTS_FILE, patients)
    storage.save_specialists(SPECIALISTS_FILE, specialists)
    storage.save_appointments(APPOINTMENTS_FILE, appointments)
    storage.save_documents(DOCUMENTS_FILE, documents)


def show_patients() -> None:
    if not patients:
        print('Пациентов нет')
        return
    for patient in sort_patients(patients):
        print(f'[{patient.id}] {patient}')


def show_specialists() -> None:
    if not specialists:
        print('Специалистов нет')
        return
    for specialist in sort_specialists(specialists):
        print(f'[{specialist.id}] {specialist}')


def show_appointments() -> None:
    if not appointments:
        print('Записей нет')
        return
    for appointment in appointments:
        print(appointment)


def create_new_appointment() -> None:
    if not patients or not specialists:
        print('Сначала добавьте пациентов и специалистов')
        return

    print('Пациенты:')
    for patient in patients:
        print(f'  [{patient.id}] {patient.get_full_name()}')

    patient_id = utils.input_int('ID пациента: ')
    patient = find_patient_by_id(patients, patient_id)
    if patient is None:
        print('Пациент не найден')
        return

    print('Специалисты:')
    for specialist in specialists:
        print(f'  [{specialist.id}] {specialist}')

    specialist_id = utils.input_int('ID специалиста: ')
    specialist = get_specialist_by_id(specialists, specialist_id)
    if specialist is None:
        print('Специалист не найден')
        return

    appointment_date = utils.input_str('Дата приёма (ГГГГ-ММ-ДД): ')
    appointment_time = utils.input_str('Время приёма (ЧЧ:ММ): ')
    complaint = utils.input_str(
        'Жалобы (необязательно): ',
        required=False,
        ) or ''

    appointment = create_appointment(
        appointments, patient, specialist,
        appointment_date, appointment_time, complaint,
    )
    if appointment is None:
        print('Этот слот уже занят')
        return
    print(f'✓ Создана запись #{appointment.id}')


def add_document_interactive() -> None:
    if not appointments:
        print('Сначала создайте хотя бы одну запись')
        return
    for appointment in appointments:
        print(f'  [{appointment.id}] {appointment}')

    appointment_id = utils.input_int('ID записи: ')
    appointment = next(
        (a for a in appointments if a.id == appointment_id), None,
    )
    if appointment is None:
        print('Запись не найдена')
        return

    document_type = utils.input_str(
        'Тип (analysis/conclusion/prescription/referral/other): ',
    )
    title = utils.input_str('Название: ')
    content = utils.input_str('Содержимое (необязательно): ',
                              required=False) or ''

    document = add_document(
        documents, appointment, document_type, title, content,
    )
    if document is None:
        print('Неверный тип документа')
        return
    print(f'✓ Добавлен документ #{document.id}')


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    load_all_data()

    print('Система управления медицинскими записями')
    print('Данные загружены.')

    while True:
        print('\nГЛАВНОЕ МЕНЮ')
        print('1. Показать пациентов')
        print('2. Показать специалистов')
        print('3. Показать записи')
        print('4. Создать запись')
        print('5. Добавить документ')
        print('6. Статистика')
        print('0. Выход')

        choice = utils.input_int('Выберите действие: ', 0, 6)

        if choice == 0:
            save_all_data()
            print('Данные сохранены. До свидания!')
            break
        elif choice == 1:
            show_patients()
        elif choice == 2:
            show_specialists()
        elif choice == 3:
            show_appointments()
        elif choice == 4:
            create_new_appointment()
        elif choice == 5:
            add_document_interactive()
        elif choice == 6:
            print(f'Пациентов: {len(patients)}')
            print(f'Специалистов: {len(specialists)}')
            print(f'Записей: {len(appointments)}')
            print(f'Документов: {len(documents)}')


if __name__ == '__main__':
    main()
