from appointments import (
    create_appointment, get_appointment_by_id,
    cancel_appointment, complete_appointment,
    get_appointment_status, is_slot_available,
    get_appointments_by_patient, get_appointments_by_specialist
)


def test_create_appointment():
    appointments = {}
    appointment_id = create_appointment(
        appointments,
        patient_id=1,
        specialist_id=1,
        appointment_date="2026-09-25",
        appointment_time="10:30",
        complaint="Боли в груди"
    )

    assert appointment_id == 1
    assert len(appointments) == 1
    assert appointments[1]["status"] == "scheduled"
    assert appointments[1]["complaint"] == "Боли в груди"


def test_get_appointment_by_id():
    appointments = {}
    appointment_id = create_appointment(
        appointments, 1, 1, "2026-09-25", "10:30")

    appointment = get_appointment_by_id(appointments, appointment_id)
    assert appointment is not None
    assert appointment["id"] == appointment_id

    appointment = get_appointment_by_id(appointments, 999)
    assert appointment is None


def test_cancel_appointment():
    appointments = {}
    appointment_id = create_appointment(
        appointments, 1, 1, "2026-09-25", "10:30")

    assert cancel_appointment(appointments, appointment_id) is True
    assert appointments[appointment_id]["status"] == "cancelled"

    # Повторная отмена невозможна
    assert cancel_appointment(appointments, appointment_id) is False

    assert cancel_appointment(appointments, 999) is False


def test_complete_appointment():
    appointments = {}
    appointment_id = create_appointment(
        appointments, 1, 1, "2026-09-25", "10:30")

    assert complete_appointment(
        appointments, appointment_id, "Диагноз", "Заметки") is True
    assert appointments[appointment_id]["status"] == "completed"
    assert appointments[appointment_id]["diagnosis"] == "Диагноз"
    assert appointments[appointment_id]["notes"] == "Заметки"


def test_get_appointment_status():
    appointment = {"status": "scheduled"}
    assert get_appointment_status(appointment) == "Запланирована"

    appointment = {"status": "completed"}
    assert get_appointment_status(appointment) == "Завершена"

    appointment = {"status": "cancelled"}
    assert get_appointment_status(appointment) == "Отменена"

    appointment = {"status": "unknown"}
    assert get_appointment_status(appointment) == "Неизвестно"


def test_is_slot_available():
    appointments = {}
    create_appointment(appointments, 1, 1, "2026-09-25", "10:30")

    assert is_slot_available(appointments, 1, "2026-09-25", "10:30") is False
    assert is_slot_available(appointments, 1, "2026-09-25", "11:00") is True
    assert is_slot_available(appointments, 2, "2026-09-25", "10:30") is True


def test_get_appointments_by_patient():
    appointments = {}
    create_appointment(appointments, 1, 1, "2026-09-25", "10:30")
    create_appointment(appointments, 1, 2, "2026-09-26", "11:00")
    create_appointment(appointments, 2, 1, "2026-09-27", "09:00")

    patient_appointments = get_appointments_by_patient(appointments, 1)
    assert len(patient_appointments) == 2

    patient_appointments = get_appointments_by_patient(appointments, 2)
    assert len(patient_appointments) == 1


def test_get_appointments_by_specialist():
    appointments = {}
    create_appointment(appointments, 1, 1, "2026-09-25", "10:30")
    create_appointment(appointments, 2, 1, "2026-09-26", "11:00")
    create_appointment(appointments, 1, 2, "2026-09-27", "09:00")

    specialist_appointments = get_appointments_by_specialist(appointments, 1)
    assert len(specialist_appointments) == 2

    specialist_appointments = get_appointments_by_specialist(appointments, 2)
    assert len(specialist_appointments) == 1
