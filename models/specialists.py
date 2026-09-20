from typing import List, Optional


class Specialist:

    def __init__(
        self,
        specialist_id: int,
        first_name: str,
        last_name: str,
        speciality: str,
        phone: str,
        email: str,
        experience_years: int = 0,
    ) -> None:
        self.id = specialist_id
        self.first_name = first_name
        self.last_name = last_name
        self.speciality = speciality
        self.phone = phone
        self.email = email
        self.experience_years = experience_years

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name}'

    def is_experienced(self) -> bool:
        return self.experience_years >= 5

    def __str__(self) -> str:
        return (f'{self.get_full_name()} ({self.speciality}), '
                f'стаж: {self.experience_years} лет')


def add_specialist(
    specialists: List[Specialist],
    first_name: str,
    last_name: str,
    speciality: str,
    phone: str,
    email: str,
    experience_years: int = 0,
) -> Specialist:
    new_id = max((s.id for s in specialists), default=0) + 1
    specialist = Specialist(
        new_id, first_name, last_name, speciality,
        phone, email, experience_years,
    )
    specialists.append(specialist)
    return specialist


def find_specialist(
    specialists: List[Specialist], query: str,
) -> List[Specialist]:
    query_lower = query.lower()
    return [
        s for s in specialists
        if query_lower in s.get_full_name().lower()
        or query_lower in s.speciality.lower()
    ]


def get_specialist_by_id(
    specialists: List[Specialist], specialist_id: int,
) -> Optional[Specialist]:
    for specialist in specialists:
        if specialist.id == specialist_id:
            return specialist
    return None


def get_all_specialists(
    specialists: List[Specialist],
) -> List[Specialist]:
    return list(specialists)


def sort_specialists(
    specialists: List[Specialist], by: str = 'last_name',
) -> List[Specialist]:
    return sorted(specialists, key=lambda s: getattr(s, by, ''))


def delete_specialist(
    specialists: List[Specialist], specialist_id: int,
) -> bool:
    specialist = get_specialist_by_id(specialists, specialist_id)
    if specialist:
        specialists.remove(specialist)
        return True
    return False
