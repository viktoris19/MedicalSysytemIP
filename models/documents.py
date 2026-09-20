from typing import List, Optional

from .appointments import Appointment

DOCUMENT_TYPES = [
    'analysis', 'conclusion', 'prescription', 'referral', 'other'
]

DOCUMENT_TYPE_MAP = {
    'analysis': 'Анализ',
    'conclusion': 'Заключение',
    'prescription': 'Рецепт',
    'referral': 'Направление',
    'other': 'Другое',
}


class Document:

    def __init__(
        self,
        document_id: int,
        appointment: Appointment,
        document_type: str,
        title: str,
        content: str = '',
        file_path: str = '',
    ) -> None:
        self.id = document_id
        self.appointment = appointment
        self.document_type = document_type
        self.title = title
        self.content = content
        self.file_path = file_path

    def get_type_display(self) -> str:
        return DOCUMENT_TYPE_MAP.get(self.document_type, self.document_type)

    def __str__(self) -> str:
        return f'#{self.id}: {self.title} ({self.get_type_display()})'


def add_document(
    documents: List[Document],
    appointment: Appointment,
    document_type: str,
    title: str,
    content: str = '',
    file_path: str = '',
) -> Optional[Document]:
    if document_type not in DOCUMENT_TYPES:
        return None
    new_id = max((d.id for d in documents), default=0) + 1
    document = Document(
        new_id, appointment, document_type, title, content, file_path,
    )
    documents.append(document)
    return document


def get_document_by_id(
    documents: List[Document], document_id: int,
) -> Optional[Document]:
    for document in documents:
        if document.id == document_id:
            return document
    return None


def get_documents_by_appointment(
    documents: List[Document], appointment: Appointment,
) -> List[Document]:
    return [d for d in documents if d.appointment.id == appointment.id]


def get_documents_by_type(
    documents: List[Document], document_type: str,
) -> List[Document]:
    return [d for d in documents if d.document_type == document_type]


def delete_document(
    documents: List[Document], document_id: int,
) -> bool:
    document = get_document_by_id(documents, document_id)
    if document:
        documents.remove(document)
        return True
    return False
