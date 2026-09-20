import json
from pathlib import Path
from typing import Any, List

from models import Appointment, Document, Patient, Specialist


def _load_json(filename: str, default: Any = None) -> Any:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                return default if default is not None else []
            return json.loads(content)
    except FileNotFoundError:
        return default if default is not None else []
    except json.JSONDecodeError:
        print(f'Ошибка: файл {filename} повреждён.')
        return default if default is not None else []


def _save_json(filename: str, data: Any) -> bool:
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except OSError as error:
        print(f'Ошибка при сохранении данных: {error}')
        return False


def load_patients(filename: str) -> List[Patient]:
    data = _load_json(filename, [])
    return [
        Patient(
            patient_id=item['id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            birth_date=item['birth_date'],
            phone=item['phone'],
            email=item['email'],
            insurance_policy=item['insurance_policy'],
            address=item.get('address', ''),
        )
        for item in data
    ]


def save_patients(filename: str, patients: List[Patient]) -> bool:
    data = [
        {
            'id': p.id,
            'first_name': p.first_name,
            'last_name': p.last_name,
            'birth_date': p.birth_date,
            'phone': p.phone,
            'email': p.email,
            'insurance_policy': p.insurance_policy,
            'address': p.address,
        }
        for p in patients
    ]
    return _save_json(filename, data)


def load_specialists(filename: str) -> List[Specialist]:
    data = _load_json(filename, [])
    return [
        Specialist(
            specialist_id=item['id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            speciality=item['speciality'],
            phone=item['phone'],
            email=item['email'],
            experience_years=item.get('experience_years', 0),
        )
        for item in data
    ]


def save_specialists(
    filename: str, specialists: List[Specialist],
) -> bool:
    data = [
        {
            'id': s.id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'speciality': s.speciality,
            'phone': s.phone,
            'email': s.email,
            'experience_years': s.experience_years,
        }
        for s in specialists
    ]
    return _save_json(filename, data)


def load_appointments(
    filename: str,
    patients: List[Patient],
    specialists: List[Specialist],
) -> List[Appointment]:
    data = _load_json(filename, [])
    patients_by_id = {p.id: p for p in patients}
    specialists_by_id = {s.id: s for s in specialists}

    appointments = []
    for item in data:
        patient = patients_by_id.get(item['patient_id'])
        specialist = specialists_by_id.get(item['specialist_id'])
        if patient is None or specialist is None:
            continue
        appointment = Appointment(
            appointment_id=item['id'],
            patient=patient,
            specialist=specialist,
            appointment_date=item['appointment_date'],
            appointment_time=item['appointment_time'],
            complaint=item.get('complaint', ''),
            diagnosis=item.get('diagnosis', ''),
            notes=item.get('notes', ''),
        )
        appointment.status = item.get('status', 'scheduled')
        appointments.append(appointment)
    return appointments


def save_appointments(
    filename: str, appointments: List[Appointment],
) -> bool:
    data = [
        {
            'id': a.id,
            'patient_id': a.patient.id,
            'specialist_id': a.specialist.id,
            'appointment_date': a.appointment_date,
            'appointment_time': a.appointment_time,
            'status': a.status,
            'complaint': a.complaint,
            'diagnosis': a.diagnosis,
            'notes': a.notes,
        }
        for a in appointments
    ]
    return _save_json(filename, data)


def load_documents(
    filename: str, appointments: List[Appointment],
) -> List[Document]:
    data = _load_json(filename, [])
    appointments_by_id = {a.id: a for a in appointments}

    documents = []
    for item in data:
        appointment = appointments_by_id.get(item['appointment_id'])
        if appointment is None:
            continue
        document = Document(
            document_id=item['id'],
            appointment=appointment,
            document_type=item['document_type'],
            title=item['title'],
            content=item.get('content', ''),
            file_path=item.get('file_path', ''),
        )
        documents.append(document)
    return documents


def save_documents(
    filename: str, documents: List[Document],
) -> bool:
    data = [
        {
            'id': d.id,
            'appointment_id': d.appointment.id,
            'document_type': d.document_type,
            'title': d.title,
            'content': d.content,
            'file_path': d.file_path,
        }
        for d in documents
    ]
    return _save_json(filename, data)
