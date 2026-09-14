from typing import Dict, List, Optional
from datetime import date


def add_patient(patients: Dict[int, dict],
                first_name: str,
                last_name: str,
                birth_date: str,
                phone: str,
                email: str,
                insurance_policy: str,
                address: str = "") -> int:
    patient_id = max(patients.keys()) + 1 if patients else 1

    patients[patient_id] = {
        "id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
        "phone": phone,
        "email": email,
        "insurance_policy": insurance_policy,
        "address": address
    }

    return patient_id


def find_patient(patients: Dict[int, dict], query: str) -> List[dict]:
    result = []
    query_lower = query.lower()

    for patient in patients.values():
        full_name = f"{patient['last_name']} {patient['first_name']}".lower()
        if query_lower in full_name or query_lower in patient.get(
                "insurance_policy", "").lower():
            result.append(patient)

    return result


def find_patient_by_policy(patients: Dict[int.dict],
                           policy: str) -> Optional[dict]:
    for patient in patients.values():
        if patient.get("insurance_policy") == policy:
            return patient

    return None


def find_patient_by_id(patients: Dict[int, dict],
                       patient_id: int) -> Optional[dict]:
    return patients.get(patient_id)


def get_patient_by_id(patients: Dict[int, dict],
                      patient_id: int) -> Optional[dict]:
    return patients.get(patient_id)


def get_all_patients(patients: Dict[int, dict]) -> List[dict]:
    return list(patients.values())


def sort_patients(patients: Dict[int, dict],
                  by: str = "last_name") -> List[dict]:
    return sorted(patients.values(), key=lambda p: p.get(by, ""))


def calculate_age(birth_date_str: str) -> int:
    try:
        birth = date.fromisoformat(birth_date_str)
        today = date.today()
        age = today.year - birth.year

        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1
        return age
    except ValueError:
        return 0


def get_patient_full_name(patient: dict) -> str:
    return f"{
        patient.get(
            'last_name',
            '')} {
        patient.get(
            'first_name',
            '')}".strip()


def delete_patient(patients: Dict[int, dict], patient_id: int) -> bool:
    if patient_id in patients:
        del patients[patient_id]
        return True
    return False
