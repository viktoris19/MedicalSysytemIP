from typing import List, Optional

from .patients import Patient
from .specialists import Specialist


class Appointment:

    STATUS_MAP = {
        'scheduled': 'Запланирована',
        'completed': 'Завершена',
        'cancelled': 'Отменена',
        'no_show': 'Не явился',
    }

    def __init__(
        self,
        appointment_id: int,
        patient: Patient,
        specialist: Specialist,
        appointment_date: str,
        appointment_time: str,
        complaint: str = '',
        diagnosis: str = '',
        notes: str = '',
    ) -> None:
        self.id = appointment_id
        self.patient = patient
        self.specialist = specialist
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = 'scheduled'
        self.complaint = complaint
        self.diagnosis = diagnosis
        self.notes = notes

    def cancel(self) -> None:
        if self.status == 'scheduled':
            self.status = 'cancelled'

    def complete(self, diagnosis: str = '', notes: str = '') -> None:
        if self.status in ['scheduled', 'no_show']:
            self.status = 'completed'
            if diagnosis:
                self.diagnosis = diagnosis
            if notes:
                self.notes = notes

    def get_status_display(self) -> str:
        return self.STATUS_MAP.get(self.status, 'Неизвестно')

    def __str__(self) -> str:
        return (f'Запись #{self.id} от {self.appointment_date} '
                f'{self.appointment_time} — {self.get_status_display()}, '
                f'пациент: {self.patient.get_full_name()}, '
                f'врач: {self.specialist.get_full_name()}')


def create_appointment(
    appointments: List[Appointment],
    patient: Patient,
    specialist: Specialist,
    appointment_date: str,
    appointment_time: str,
    complaint: str = '',
) -> Optional[Appointment]:
    if not is_slot_available(
        appointments, specialist, appointment_date, appointment_time,
    ):
        return None
    new_id = max((a.id for a in appointments), default=0) + 1
    appointment = Appointment(
        new_id, patient, specialist,
        appointment_date, appointment_time, complaint,
    )
    appointments.append(appointment)
    return appointment


def get_appointment_by_id(
    appointments: List[Appointment], appointment_id: int,
) -> Optional[Appointment]:
    for appointment in appointments:
        if appointment.id == appointment_id:
            return appointment
    return None


def is_slot_available(
    appointments: List[Appointment],
    specialist: Specialist,
    appointment_date: str,
    appointment_time: str,
) -> bool:
    for app in appointments:
        if (app.specialist.id == specialist.id
                and app.appointment_date == appointment_date
                and app.appointment_time == appointment_time
                and app.status != 'cancelled'):
            return False
    return True


def get_appointments_by_patient(
    appointments: List[Appointment], patient: Patient,
) -> List[Appointment]:
    return [a for a in appointments if a.patient.id == patient.id]


def get_appointments_by_specialist(
    appointments: List[Appointment], specialist: Specialist,
) -> List[Appointment]:
    return [a for a in appointments if a.specialist.id == specialist.id]


def cancel_appointment(
    appointments: List[Appointment], appointment_id: int,
) -> bool:
    appointment = get_appointment_by_id(appointments, appointment_id)
    if appointment and appointment.status == 'scheduled':
        appointment.cancel()
        return True
    return False


def complete_appointment(
    appointments: List[Appointment],
    appointment_id: int,
    diagnosis: str = '',
    notes: str = '',
) -> bool:
    appointment = get_appointment_by_id(appointments, appointment_id)
    if appointment and appointment.status in ['scheduled', 'no_show']:
        appointment.complete(diagnosis, notes)
        return True
    return False


def get_all_appointments(
    appointments: List[Appointment],
) -> List[Appointment]:
    return list(appointments)


def get_appointments_by_status(
    appointments: List[Appointment], status: str,
) -> List[Appointment]:
    return [a for a in appointments if a.status == status]


def delete_appointment(
    appointments: List[Appointment], appointment_id: int,
) -> bool:
    appointment = get_appointment_by_id(appointments, appointment_id)
    if appointment:
        appointments.remove(appointment)
        return True
    return False
