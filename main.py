import os
from typing import Dict

import patients as pat
import specialists as spec
import appointments as appt
import documents as doc
import storage as st
import utils

DATA_DIR = "data"
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
SPECIALISTS_FILE = os.path.join(DATA_DIR, "specialists.json")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")

patients: Dict[int, dict] = {}
specialists: Dict[int, dict] = {}
appointments: Dict[int, dict] = {}
documents: Dict[int, dict] = {}


def load_all_data() -> None:
    global patients, specialists, appointments, documents

    patients = st.load_patients(PATIENTS_FILE)
    specialists = st.load_specialists(SPECIALISTS_FILE)
    appointments = st.load_appointments(APPOINTMENTS_FILE)
    documents = st.load_documents(DOCUMENTS_FILE)


def save_all_data() -> None:
    st.save_patients(PATIENTS_FILE, patients)
    st.save_specialists(SPECIALISTS_FILE, specialists)
    st.save_appointments(APPOINTMENTS_FILE, appointments)
    st.save_documents(DOCUMENTS_FILE, documents)


def show_main_menu() -> None:
    print("\n" + "=" * 55)
    print("СИСТЕМА УПРАВЛЕНИЯ МЕДИЦИНСКИМИ ЗАПИСЯМИ")
    print("=" * 55)
    print("\nГЛАВНОЕ МЕНЮ:")
    print("  1. Управление пациентами")
    print("  2. Управление специалистами")
    print("  3. Управление записями")
    print("  4. Управление документами")
    print("  5. Просмотр статистики")
    print("  0. Выход")
    print("=" * 55)


def show_patients_menu() -> None:
    while True:
        print("\n--- УПРАВЛЕНИЕ ПАЦИЕНТАМИ ---")
        print("  1. Добавить пациента")
        print("  2. Поиск пациентов")
        print("  3. Показать всех пациентов")
        print("  4. Удалить пациента")
        print("  0. Назад")

        choice = utils.input_int("Выберите действие: ", 0, 4)

        if choice == 0:
            break
        elif choice == 1:
            add_patient_interactive()
        elif choice == 2:
            find_patients_interactive()
        elif choice == 3:
            show_all_patients()
        elif choice == 4:
            delete_patient_interactive()

        save_all_data()


def add_patient_interactive() -> None:
    print("\n--- ДОБАВЛЕНИЕ ПАЦИЕНТА ---")

    first_name = utils.input_str("Имя: ")
    last_name = utils.input_str("Фамилия: ")
    birth_date_str = utils.input_str("Дата рождения (ГГГГ-ММ-ДД): ")
    phone = utils.input_str("Телефон: ")
    email = utils.input_str("Email: ")
    insurance_policy = utils.input_str("Номер полиса: ")
    address = utils.input_str("Адрес (необязательно): ", required=False) or ""

    patient_id = pat.add_patient(
        patients, first_name, last_name, birth_date_str,
        phone, email, insurance_policy, address
    )

    print(f"✓ Пациент добавлен с ID: {patient_id}")


def find_patients_interactive() -> None:
    query = utils.input_str("Введите поисковый запрос (ФИО или полис): ")
    results = pat.find_patient(patients, query)

    if not results:
        print("Пациенты не найдены")
        return

    print(f"\nНайдено пациентов: {len(results)}")
    print("-" * 60)
    for p in sorted(results, key=lambda x: x['last_name']):
        age = pat.calculate_age(p['birth_date'])
        print(
            f"ID: {p['id']} | {p['last_name']} {p['first_name']}"
            f"| {age} лет | Полис: {p['insurance_policy']}")


def show_all_patients() -> None:
    patients_list = pat.get_all_patients(patients)
    if not patients_list:
        print("Пациентов нет")
        return

    print(f"\nВсего пациентов: {len(patients_list)}")
    print("-" * 60)
    for p in pat.sort_patients(patients):
        age = pat.calculate_age(p['birth_date'])
        print(
            f"ID: {p['id']} | {p['last_name']} {p['first_name']}"
            f"| {age} лет | {p['phone']}")


def delete_patient_interactive() -> None:
    patient_id = utils.input_int("Введите ID пациента для удаления: ")
    patient = pat.get_patient_by_id(patients, patient_id)

    if not patient:
        print("Пациент не найден")
        return

    full_name = pat.get_patient_full_name(patient)
    confirm = input(f"Удалить пациента {full_name}? (д/н): ").lower()

    if confirm == 'д':
        if pat.delete_patient(patients, patient_id):
            print(f"✓ Пациент {full_name} удален")


def show_specialists_menu() -> None:
    while True:
        print("\n--- УПРАВЛЕНИЕ СПЕЦИАЛИСТАМИ ---")
        print("  1. Добавить специалиста")
        print("  2. Поиск специалистов")
        print("  3. Показать всех специалистов")
        print("  4. Удалить специалиста")
        print("  0. Назад")

        choice = utils.input_int("Выберите действие: ", 0, 4)

        if choice == 0:
            break
        elif choice == 1:
            add_specialist_interactive()
        elif choice == 2:
            find_specialists_interactive()
        elif choice == 3:
            show_all_specialists()
        elif choice == 4:
            delete_specialist_interactive()

        save_all_data()


def add_specialist_interactive() -> None:
    print("\n--- ДОБАВЛЕНИЕ СПЕЦИАЛИСТА ---")

    first_name = utils.input_str("Имя: ")
    last_name = utils.input_str("Фамилия: ")
    speciality = utils.input_str("Специальность: ")
    phone = utils.input_str("Телефон: ")
    email = utils.input_str("Email: ")
    experience = utils.input_int("Стаж (лет): ", 0)

    specialist_id = spec.add_specialist(
        specialists, first_name, last_name, speciality,
        phone, email, experience
    )

    print(f"✓ Специалист добавлен с ID: {specialist_id}")


def find_specialists_interactive() -> None:
    query = utils.input_str(
        "Введите поисковый запрос (ФИО или специальность): ")
    results = spec.find_specialist(specialists, query)

    if not results:
        print("Специалисты не найдены")
        return

    print(f"\nНайдено специалистов: {len(results)}")
    print("-" * 60)
    for s in sorted(results, key=lambda x: x['last_name']):
        print(
            f"ID: {s['id']} | {s['last_name']} {s['first_name']}"
            f"| {s['speciality']} | Стаж: {s['experience_years']} лет")


def show_all_specialists() -> None:
    specialists_list = spec.get_all_specialists(specialists)
    if not specialists_list:
        print("Специалистов нет")
        return

    print(f"\nВсего специалистов: {len(specialists_list)}")
    print("-" * 60)
    for s in spec.sort_specialists(specialists):
        print(
            f"ID: {s['id']} | {s['last_name']} {s['first_name']}"
            f" {s['speciality']} | Стаж: {s['experience_years']} лет")


def delete_specialist_interactive() -> None:
    specialist_id = utils.input_int("Введите ID специалиста для удаления: ")
    specialist = spec.get_specialist_by_id(specialists, specialist_id)

    if not specialist:
        print("Специалист не найден")
        return

    full_name = spec.get_specialist_full_name(specialist)
    confirm = input(f"Удалить специалиста {full_name}? (д/н): ").lower()

    if confirm == 'д':
        if spec.delete_specialist(specialists, specialist_id):
            print(f"✓ Специалист {full_name} удален")


def show_appointments_menu() -> None:
    while True:
        print("\n--- УПРАВЛЕНИЕ ЗАПИСЯМИ ---")
        print("  1. Создать запись")
        print("  2. Показать все записи")
        print("  3. Поиск записей по пациенту")
        print("  4. Поиск записей по специалисту")
        print("  5. Отменить запись")
        print("  6. Завершить запись")
        print("  0. Назад")

        choice = utils.input_int("Выберите действие: ", 0, 6)

        if choice == 0:
            break
        elif choice == 1:
            create_appointment_interactive()
        elif choice == 2:
            show_all_appointments()
        elif choice == 3:
            show_appointments_by_patient()
        elif choice == 4:
            show_appointments_by_specialist()
        elif choice == 5:
            cancel_appointment_interactive()
        elif choice == 6:
            complete_appointment_interactive()

        save_all_data()


def create_appointment_interactive() -> None:
    print("\n--- СОЗДАНИЕ ЗАПИСИ ---")

    if not patients or not specialists:
        print("Ошибка: добавьте сначала пациентов и специалистов")
        return

    print("\nСписок пациентов:")
    for p in pat.get_all_patients(patients):
        print(f"  {p['id']}: {p['last_name']} {p['first_name']}")
    patient_id = utils.input_int("ID пациента: ")

    if patient_id not in patients:
        print("Ошибка: пациент не найден")
        return

    print("\nСписок специалистов:")
    for s in spec.get_all_specialists(specialists):
        print(
            f"  {
                s['id']}: {
                s['last_name']} {
                s['first_name']} ({
                    s['speciality']})")
    specialist_id = utils.input_int("ID специалиста: ")

    if specialist_id not in specialists:
        print("Ошибка: специалист не найден")
        return

    appointment_date = utils.input_str("Дата приема (ГГГГ-ММ-ДД): ")
    appointment_time = utils.input_str("Время приема (ЧЧ:ММ): ")

    if not appt.is_slot_available(appointments, specialist_id,
                                  appointment_date, appointment_time):
        print("Ошибка: этот слот уже занят")
        return

    complaint = utils.input_str(
        "Жалобы (необязательно): ", required=False) or ""

    appointment_id = appt.create_appointment(
        appointments, patient_id, specialist_id,
        appointment_date, appointment_time, complaint
    )

    print(f"✓ Запись создана с ID: {appointment_id}")


def show_all_appointments() -> None:
    appointments_list = appt.get_all_appointments(appointments)
    if not appointments_list:
        print("Записей нет")
        return

    print(f"\nВсего записей: {len(appointments_list)}")
    print("-" * 70)
    for a in sorted(appointments_list, key=lambda x: x['appointment_date']):
        patient = pat.get_patient_by_id(patients, a['patient_id'])
        specialist = spec.get_specialist_by_id(specialists, a['specialist_id'])
        patient_name = pat.get_patient_full_name(
            patient) if patient else "Неизвестен"
        specialist_name = spec.get_specialist_full_name(
            specialist) if specialist else "Неизвестен"
        status = appt.get_appointment_status(a)
        print(f"#{a['id']} | {a['appointment_date']} {a['appointment_time']}")
        print(
            f"  Пациент: {patient_name} | Врач: {specialist_name}"
            f"| Статус: {status}")


def show_appointments_by_patient() -> None:
    patient_id = utils.input_int("Введите ID пациента: ")
    patient = pat.get_patient_by_id(patients, patient_id)

    if not patient:
        print("Пациент не найден")
        return

    patient_appointments = appt.get_appointments_by_patient(
        appointments, patient_id)

    if not patient_appointments:
        print(f"У пациента {pat.get_patient_full_name(patient)} нет записей")
        return

    print(f"\nЗаписи пациента {pat.get_patient_full_name(patient)}:")
    print("-" * 60)
    for a in sorted(patient_appointments, key=lambda x: x['appointment_date']):
        specialist = spec.get_specialist_by_id(specialists, a['specialist_id'])
        specialist_name = spec.get_specialist_full_name(
            specialist) if specialist else "Неизвестен"
        print(f"  #{a['id']}: {a['appointment_date']} {a['appointment_time']}"
              f"| {specialist_name} | {appt.get_appointment_status(a)}")


def show_appointments_by_specialist() -> None:
    specialist_id = utils.input_int("Введите ID специалиста: ")
    specialist = spec.get_specialist_by_id(specialists, specialist_id)

    if not specialist:
        print("Специалист не найден")
        return

    specialist_appointments = appt.get_appointments_by_specialist(
        appointments, specialist_id)

    if not specialist_appointments:
        print(
            f"У специалиста {
                spec.get_specialist_full_name(specialist)} нет записей")
        return

    print(
        f"\nЗаписи к специалисту {spec.get_specialist_full_name(specialist)}:")
    print("-" * 60)
    for a in sorted(
            specialist_appointments,
            key=lambda x: x['appointment_date']):
        patient = pat.get_patient_by_id(patients, a['patient_id'])
        patient_name = pat.get_patient_full_name(
            patient) if patient else "Неизвестен"
        print(f"  #{a['id']}: {a['appointment_date']} {a['appointment_time']}"
              f"| {patient_name} | {appt.get_appointment_status(a)}")


def cancel_appointment_interactive() -> None:
    appointment_id = utils.input_int("Введите ID записи для отмены: ")

    if appt.cancel_appointment(appointments, appointment_id):
        print(f"✓ Запись #{appointment_id} отменена")
    else:
        print("Ошибка: запись не найдена или уже отменена")


def complete_appointment_interactive() -> None:
    appointment_id = utils.input_int("Введите ID записи для завершения: ")

    if appointment_id not in appointments:
        print("Запись не найдена")
        return

    diagnosis = utils.input_str("Диагноз: ", required=False) or ""
    notes = utils.input_str("Заметки (необязательно): ", required=False) or ""

    if appt.complete_appointment(
            appointments,
            appointment_id,
            diagnosis,
            notes):
        print(f"✓ Запись #{appointment_id} завершена")
    else:
        print("Ошибка: запись не может быть завершена")


def show_statistics() -> None:
    print("\n" + "=" * 55)
    print("СТАТИСТИКА СИСТЕМЫ")
    print("=" * 55)

    total_patients = len(patients)
    total_specialists = len(specialists)
    total_appointments = len(appointments)
    total_documents = len(documents)

    print(f"Пациентов: {total_patients}")
    print(f"Специалистов: {total_specialists}")
    print(f"Записей: {total_appointments}")
    print(f"Документов: {total_documents}")

    if total_appointments > 0:
        print("\nЗаписи по статусам:")
        statuses = ["scheduled", "completed", "cancelled", "no_show"]
        for status in statuses:
            count = len(appt.get_appointments_by_status(appointments, status))
            if count > 0:
                status_display = appt.get_appointment_status(
                    {"status": status})
                print(f"  {status_display}: {count}")

    if total_documents > 0:
        print("\nДокументы по типам:")
        for doc_type in doc.DOCUMENT_TYPES:
            count = len(doc.get_documents_by_type(documents, doc_type))
            if count > 0:
                print(f"  {doc.get_document_type_display(doc_type)}: {count}")

    print("=" * 55)


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    load_all_data()

    print("\n" + "=" * 55)
    print("СИСТЕМА УПРАВЛЕНИЯ МЕДИЦИНСКИМИ ЗАПИСЯМИ")
    print("=" * 55)
    print("Данные загружены. Для работы используйте меню.")

    while True:
        show_main_menu()
        choice = utils.input_int("Выберите действие: ", 0, 5)

        if choice == 0:
            print("\nСохранение данных...")
            save_all_data()
            print("Данные сохранены. До свидания!")
            break
        elif choice == 1:
            show_patients_menu()
        elif choice == 2:
            show_specialists_menu()
        elif choice == 3:
            show_appointments_menu()
        elif choice == 4:
            show_documents_menu()
        elif choice == 5:
            show_statistics()


def show_documents_menu() -> None:
    while True:
        print("\n--- УПРАВЛЕНИЕ ДОКУМЕНТАМИ ---")
        print("  1. Добавить документ")
        print("  2. Показать документы записи")
        print("  3. Показать все документы")
        print("  0. Назад")

        choice = utils.input_int("Выберите действие: ", 0, 3)

        if choice == 0:
            break
        elif choice == 1:
            add_document_interactive()
        elif choice == 2:
            show_documents_by_appointment()
        elif choice == 3:
            show_all_documents()

        save_all_data()


def add_document_interactive() -> None:
    print("\n--- ДОБАВЛЕНИЕ ДОКУМЕНТА ---")

    appointment_id = utils.input_int("ID записи: ")
    if appointment_id not in appointments:
        print("Ошибка: запись не найдена")
        return

    print("\nТипы документов:")
    for dt in doc.DOCUMENT_TYPES:
        print(f"  {dt} - {doc.get_document_type_display(dt)}")

    document_type = utils.input_str("Тип документа: ")
    if document_type not in doc.DOCUMENT_TYPES:
        print("Ошибка: неверный тип документа")
        return

    title = utils.input_str("Название документа: ")
    content = utils.input_str(
        "Содержание (необязательно): ", required=False) or ""
    file_path = utils.input_str(
        "Путь к файлу (необязательно): ", required=False) or ""

    document_id = doc.add_document(
        documents, appointment_id, document_type, title, content, file_path
    )

    if document_id:
        print(f"✓ Документ добавлен с ID: {document_id}")
    else:
        print("Ошибка при добавлении документа")


def show_documents_by_appointment() -> None:
    appointment_id = utils.input_int("Введите ID записи: ")
    documents_list = doc.get_documents_by_appointment(
        documents, appointment_id)

    if not documents_list:
        print("Документов для этой записи нет")
        return

    print(f"\nДокументы записи #{appointment_id}:")
    print("-" * 60)
    for d in documents_list:
        print(
            f"  #{d['id']}: {d['title']}"
            f"| {doc.get_document_type_display(d['document_type'])}")


def show_all_documents() -> None:
    documents_list = list(documents.values())
    if not documents_list:
        print("Документов нет")
        return

    print(f"\nВсего документов: {len(documents_list)}")
    print("-" * 60)
    for d in documents_list:
        appointment = appointments.get(d['appointment_id'])
        appointment_info = f"Запись #{
            d['appointment_id']}" if appointment else "Запись удалена"
        print(
            f"  #{
                d['id']}: {
                d['title']}" f"| {
                doc.get_document_type_display(
                    d['document_type'])} | {appointment_info}")


if __name__ == "__main__":
    main()
