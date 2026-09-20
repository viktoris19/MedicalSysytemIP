from datetime import date
from typing import List, Optional


class Patient:

    def __init__(
        self,
        patient_id: int,
        first_name: str,
        last_name: str,
        birth_date: str,
        phone: str,
        email: str,
        insurance_policy: str,
        address: str = '',
    ) -> None:
        self.id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.insurance_policy = insurance_policy
        self.address = address

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name}'

    def get_age(self) -> int:
        try:
            birth = date.fromisoformat(self.birth_date)
        except ValueError:
            return 0
        today = date.today()
        age = today.year - birth.year
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1
        return age

    def __str__(self) -> str:
        return (f'{self.get_full_name()}, '
                f'{self.get_age()} лет, полис: {self.insurance_policy}')


def add_patient(
    patients: List[Patient],
    first_name: str,
    last_name: str,
    birth_date: str,
    phone: str,
    email: str,
    insurance_policy: str,
    address: str = '',
) -> Patient:
    new_id = max((p.id for p in patients), default=0) + 1
    patient = Patient(
        new_id, first_name, last_name, birth_date,
        phone, email, insurance_policy, address,
    )
    patients.append(patient)
    return patient


def find_patient(patients: List[Patient], query: str) -> List[Patient]:
    query_lower = query.lower()
    return [
        p for p in patients
        if query_lower in p.get_full_name().lower()
        or query_lower in p.insurance_policy.lower()
    ]


def find_patient_by_id(
    patients: List[Patient], patient_id: int,
) -> Optional[Patient]:
    for patient in patients:
        if patient.id == patient_id:
            return patient
    return None


def get_all_patients(patients: List[Patient]) -> List[Patient]:
    return list(patients)


def sort_patients(
    patients: List[Patient], by: str = 'last_name',
) -> List[Patient]:
    return sorted(patients, key=lambda p: getattr(p, by, ''))


def delete_patient(patients: List[Patient], patient_id: int) -> bool:
    patient = find_patient_by_id(patients, patient_id)
    if patient:
        patients.remove(patient)
        return True
    return False
