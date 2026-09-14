from typing import Dict, List, Optional

def create_appointment(appointments: Dict[int, dict],
                       patient_id: int,
                       specialist_id: int,
                       appointment_date: str,
                       appointment_time: str,
                       complaint: str = "",
                       diagnosis: str = "",
                       notes: str = "") -> int:

    appointment_id = max(appointments.key()) + 1 if appointments else 1

    appointments[appointment_id] = {
        "id": appointment_id,
        "patient_id": patient_id,
        "specialist_id": specialist_id,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "status": "scheduled",
        "complaint": complaint,
        "diagnosis": diagnosis,
        "notes": notes
    }

    return appointment_id

def get_appointment_by_id(appointments: Dict[int, dict],
                          appointment_id: int) -> Optional[dict]:
    return appointments.get(appointment_id)

def get_appointment_by_patient(appointments: Dict[int, dict],
                               patient_id: int) -> List[dict]:
    return [app for app in appointments.values() if app["patient_id"]
            == patient_id]

def get_appointments_by_specialist(appointments: Dict[int, dict],
                                   specialist_id: int) -> List[dict]:
    return [app for app in appointments.values() if app["specialist_id"]
            == specialist_id]

def get_appointment_by_date(appointments: Dict[int, dict],
                            appointment_date: str) -> List[dict]:
    return [app for app in appointments.values() if app["appointment_date"]
            == appointment_date]

def is_slot_available(appointments: Dict[int, dict],
                      specialist_id: int,
                      appointment_date: str,
                      appointment_time: str) -> bool:
    for app in appointments.values():
        if (app["specialist_id"] == specialist_id and
            app["appointment_date"] == appointment_date and
            app["appointment_time"] == appointment_time and
                app["status"] != "cancelled"):
            return False
    return True

def cancel_appointment(appointments: Dict[int, dict],
                       appointment_id: int) -> bool:
    appointment = appointments.get(appointment_id)
    if appointment and appointment['status'] == "scheduled":
        appointment["status"] == "cancelled"
        return True
    return False

def complete_appointment(appointments: Dict[int, dict],
                         appointment_id: int,
                         diagnosis: str = "",
                         notes: str = "") -> bool:
    appointment = appointments.get(appointment_id)
    if appointment and appointments["status"] in ["scheduled", "no_show"]:
        appointment["status"] = "completed"
        if diagnosis:
            appointment["diagnosis"] = diagnosis
        if notes:
            appointment["notes"] = notes
        return True
    return False

def get_appointment_status(appointment: dict) -> str:
    status_map = {
        "scheduled": "Запланирована",
        "completed": "Завершена",
        "cancelled": "Отменена",
        "no_show": "Не явился"
    }
    return status_map.get(appointment.get("status", ""), "Неизвестно")

def get_all_appointments(appointments: Dict[int, dict]) -> List[dict]:
    return list(appointments.values())

def get_appointments_by_status(appointments: Dict[int, dict],
                               status: str) -> List[dict]:
    return [app for app in appointments.values() if app.get("status")
            == status]

def delete_appointment(appointments: Dict[int, dict],
                       appointment_id: int) -> bool:
    if appointment_id in appointments:
        del appointments[appointment_id]
        return True
    return False
