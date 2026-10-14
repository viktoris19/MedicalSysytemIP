import json

from db.database import get_connection

PATIENTS_FILE = 'data/patients.json'
SPECIALISTS_FILE = 'data/specialists.json'
APPOINTMENTS_FILE = 'data/appointments.json'
DOCUMENTS_FILE = 'data/documents.json'


def load_json(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def import_patients(conn) -> None:
    patients = load_json(PATIENTS_FILE)
    conn.executemany(
        """
        INSERT INTO patients (
            id, first_name, last_name, birth_date,
            phone, email, insurance_policy, address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                patient['id'],
                patient['first_name'],
                patient['last_name'],
                patient['birth_date'],
                patient['phone'],
                patient['email'],
                patient['insurance_policy'],
                patient.get('address', ''),
            )
            for patient in patients
        ],
    )


def import_specialists(conn) -> None:
    specialists = load_json(SPECIALISTS_FILE)
    conn.executemany(
        """
        INSERT INTO specialists (
            id, first_name, last_name, speciality,
            phone, email, experience_years
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                specialist['id'],
                specialist['first_name'],
                specialist['last_name'],
                specialist['speciality'],
                specialist['phone'],
                specialist['email'],
                specialist.get('experience_years', 0),
            )
            for specialist in specialists
        ],
    )


def import_appointments(conn) -> None:
    appointments = load_json(APPOINTMENTS_FILE)
    conn.executemany(
        """
        INSERT INTO appointments (
            id, patient_id, specialist_id,
            appointment_date, appointment_time,
            status, complaint, diagnosis, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                appointment['id'],
                appointment['patient_id'],
                appointment['specialist_id'],
                appointment['appointment_date'],
                appointment['appointment_time'],
                appointment.get('status', 'scheduled'),
                appointment.get('complaint', ''),
                appointment.get('diagnosis', ''),
                appointment.get('notes', ''),
            )
            for appointment in appointments
        ],
    )


def import_documents(conn) -> None:
    documents = load_json(DOCUMENTS_FILE)
    conn.executemany(
        """
        INSERT INTO documents (
            id, appointment_id, document_type,
            title, content, file_path
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                document['id'],
                document['appointment_id'],
                document['document_type'],
                document['title'],
                document.get('content', ''),
                document.get('file_path', ''),
            )
            for document in documents
        ],
    )


def main() -> None:
    conn = get_connection()
    try:
        import_patients(conn)
        import_specialists(conn)
        import_appointments(conn)
        import_documents(conn)
        conn.commit()
        print('Данные успешно импортированы')
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()