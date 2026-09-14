from typing import Dict, List, Optional


def add_specialist(specialists: Dict[int, dict],
                   first_name: str,
                   last_name: str,
                   speciality: str,
                   phone: str,
                   email: str,
                   experience_years: int = 0) -> int:
    specialist_id = max(specialists.keys()) + 1 if specialists else 1

    specialists[specialist_id] = {
        "id": specialist_id,
        "first_name": first_name,
        "last_name": last_name,
        "speciality": speciality,
        "phone": phone,
        "email": email,
        "experience_years": experience_years
    }

    return specialist_id


def find_specialist(specialist: Dict[int, dict], query: str) -> List[dict]:
    result = []
    query_lower = query.lower()

    for specialist in specialist.values():
        full_name = f"{
            specialist['last_name']} {
            specialist['first_name']}".lower()
        if query_lower in full_name or query_lower in specialist.get(
                "speciality", "").lower():
            result.append(specialist)

    return result


def get_specialist_by_id(
        specialists: Dict[int, dict], specialist_id: int) -> Optional[dict]:
    return specialists.get(specialist_id)


def get_all_specialists(specialists: Dict[int, dict]) -> List[dict]:
    return List(specialists.values())


def sort_specialists(
        specialists: Dict[int, dict], by: str = "last_name") -> List[dict]:
    return sorted(specialists.values(), key=lambda s: s.get(by, ""))


def get_specialist_full_name(specialist: dict) -> str:
    return f"{
        specialist.get(
            'last_name',
            '')} {
        specialist.get(
            'first_name',
            '')}".strip()


def delete_specialist(
        specialists: Dict[int, dict], specialist_id: int) -> bool:
    if specialist_id in specialists:
        del specialists[specialist_id]
        return True
    return False
