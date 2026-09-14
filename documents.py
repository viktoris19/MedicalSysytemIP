from typing import Dict, List, Optional

DOCUMENT_TYPES = ["analysis", "conclusion",
                  "prescription", "referral", "other"]


def add_document(documents: Dict[int, dict],
                 appointment_id: int,
                 document_type: str,
                 title: str,
                 content: str = "",
                 file_path: str = "") -> Optional[int]:
    if document_type not in DOCUMENT_TYPES:
        return None

    document_id = max(documents.keys()) + 1 if documents else 1

    documents[document_id] = {
        "id": document_id,
        "appointment_id": appointment_id,
        "document_type": document_type,
        "title": title,
        "content": content,
        "file_path": file_path
    }

    return document_id


def get_document_by_id(documents: Dict[int, dict],
                       document_id: int) -> Optional[dict]:
    return documents.get(document_id)


def get_document_by_appointment(documents: Dict[int, dict],
                                appointment_id: int) -> List[dict]:
    return [doc for doc in documents.values() if doc["appointment_id"]
            == appointment_id]


def get_documents_by_type(documents: Dict[int, dict],
                          document_type: str) -> List[dict]:
    return [doc for doc in documents.values() if doc.get(
        "document_type") == document_type]


def get_document_type_display(document_type: str) -> str:
    type_map = {
        "analysis": "Анализ",
        "conclusion": "Заключение",
        "prescription": "Рецепт",
        "referral": "Направление",
        "other": "Другое"
    }
    return type_map.get(document_type, document_type)


def delete_document(documents: Dict[int, dict],
                    document_id: int) -> bool:
    if document_id in documents:
        del documents[document_id]
        return True
    return False
