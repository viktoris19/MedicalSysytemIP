from models import Appointment, Patient, Specialist
from models.appointments import (
    cancel_appointment,
    complete_appointment,
    create_appointment,
    get_appointments_by_patient,
    get_appointments_by_specialist,
    is_slot_available,
)


def _make_patient(patient_id: int = 1, name: str = 'Иван') -> Patient:
    return Patient(
        patient_id, name, 'Смирнов', '1985-06-15',
        '+79990000000', 'test@mail.ru', f'POLICY-{patient_id}',
    )


def _make_specialist(
    specialist_id: int = 1, speciality: str = 'Кардиолог',
) -> Specialist:
    return Specialist(
        specialist_id, 'Анна', 'Петрова', speciality,
        '+79991234567', f'doc{specialist_id}@clinic.ru', 10,
    )


def test_appointment_creation():
    patient = _make_patient()
    specialist = _make_specialist()
    appointment = Appointment(
        1, patient, specialist, '2026-09-25', '10:30',
        complaint='Боли в груди',
    )
    assert appointment.id == 1
    assert appointment.patient is patient
    assert appointment.specialist is specialist
    assert appointment.status == 'scheduled'


def test_appointment_cancel():
    patient = _make_patient()
    specialist = _make_specialist()
    appointment = Appointment(
        1, patient, specialist, '2026-09-25', '10:30',
    )
    appointment.cancel()
    assert appointment.status == 'cancelled'


def test_appointment_complete():
    patient = _make_patient()
    specialist = _make_specialist()
    appointment = Appointment(
        1, patient, specialist, '2026-09-25', '10:30',
    )
    appointment.complete('Диагноз', 'Заметки')
    assert appointment.status == 'completed'
    assert appointment.diagnosis == 'Диагноз'
    assert appointment.notes == 'Заметки'


def test_appointment_str():
    patient = _make_patient()
    specialist = _make_specialist()
    appointment = Appointment(
        1, patient, specialist, '2026-09-25', '10:30',
    )
    text = str(appointment)
    assert 'Запись #1' in text
    assert 'Смирнов Иван' in text
    assert 'Петрова Анна' in text


def test_is_slot_available():
    patient = _make_patient()
    specialist = _make_specialist()
    appointments = []
    create_appointment(
        appointments, patient, specialist, '2026-09-25', '10:30',
    )
    assert is_slot_available(
        appointments, specialist, '2026-09-25', '10:30',
    ) is False
    assert is_slot_available(
        appointments, specialist, '2026-09-25', '11:00',
    ) is True


def test_create_appointment():
    patient = _make_patient()
    specialist = _make_specialist()
    appointments = []
    appointment = create_appointment(
        appointments, patient, specialist, '2026-09-25', '10:30',
    )
    assert appointment is not None
    assert len(appointments) == 1

    duplicate = create_appointment(
        appointments, patient, specialist, '2026-09-25', '10:30',
    )
    assert duplicate is None
    assert len(appointments) == 1


def test_cancel_appointment():
    patient = _make_patient()
    specialist = _make_specialist()
    appointments = []
    appointment = create_appointment(
        appointments, patient, specialist, '2026-09-25', '10:30',
    )
    assert cancel_appointment(appointments, appointment.id) is True
    assert appointment.status == 'cancelled'

    assert cancel_appointment(appointments, appointment.id) is False
    assert cancel_appointment(appointments, 999) is False


def test_complete_appointment():
    patient = _make_patient()
    specialist = _make_specialist()
    appointments = []
    appointment = create_appointment(
        appointments, patient, specialist, '2026-09-25', '10:30',
    )
    assert complete_appointment(
        appointments, appointment.id, 'Диагноз', 'Заметки',
    ) is True
    assert appointment.status == 'completed'


def test_appointments_by_patient():
    patient1 = _make_patient(1, 'Иван')
    patient2 = _make_patient(2, 'Ольга')
    specialist = _make_specialist()
    appointments = []
    create_appointment(appointments, patient1, specialist,
                       '2026-09-25', '10:30')
    create_appointment(appointments, patient1, specialist,
                       '2026-09-26', '11:00')
    create_appointment(appointments, patient2, specialist,
                       '2026-09-27', '09:00')

    assert len(get_appointments_by_patient(appointments, patient1)) == 2
    assert len(get_appointments_by_patient(appointments, patient2)) == 1


def test_appointments_by_specialist():
    patient = _make_patient()
    spec1 = _make_specialist(1, 'Кардиолог')
    spec2 = _make_specialist(2, 'Терапевт')
    appointments = []
    create_appointment(appointments, patient, spec1,
                       '2026-09-25', '10:30')
    create_appointment(appointments, patient, spec1,
                       '2026-09-26', '11:00')
    create_appointment(appointments, patient, spec2,
                       '2026-09-27', '09:00')

    assert len(get_appointments_by_specialist(appointments, spec1)) == 2
    assert len(get_appointments_by_specialist(appointments, spec2)) == 1