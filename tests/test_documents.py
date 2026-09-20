from models import Appointment, Document, Patient, Specialist
from models.documents import (
    add_document,
    delete_document,
    get_document_by_id,
    get_documents_by_appointment,
    get_documents_by_type,
)


def _make_appointment(appointment_id: int = 1) -> Appointment:
    patient = Patient(
        1, 'Иван', 'Смирнов', '1985-06-15',
        '+79990000000', 'ivan@mail.ru', 'POLICY-1',
    )
    specialist = Specialist(
        1, 'Анна', 'Петрова', 'Кардиолог',
        '+79991234567', 'petrova@clinic.ru', 10,
    )
    return Appointment(
        appointment_id, patient, specialist, '2026-09-25', '10:30',
    )


def test_document_creation():
    appointment = _make_appointment()
    document = Document(
        1, appointment, 'analysis', 'ЭКГ',
        content='Синусовый ритм',
    )
    assert document.id == 1
    assert document.appointment is appointment
    assert document.title == 'ЭКГ'


def test_document_type_display():
    appointment = _make_appointment()
    document = Document(1, appointment, 'analysis', 'ЭКГ')
    assert document.get_type_display() == 'Анализ'


def test_document_str():
    appointment = _make_appointment()
    document = Document(1, appointment, 'prescription', 'Рецепт')
    assert 'Рецепт' in str(document)
    assert 'Рецепт' in document.get_type_display()


def test_add_document():
    appointment = _make_appointment()
    documents = []
    document = add_document(
        documents, appointment, 'analysis', 'ЭКГ',
    )
    assert document is not None
    assert len(documents) == 1


def test_add_document_invalid_type():
    appointment = _make_appointment()
    documents = []
    document = add_document(
        documents, appointment, 'unknown', 'Что-то',
    )
    assert document is None
    assert len(documents) == 0


def test_get_document_by_id():
    appointment = _make_appointment()
    documents = []
    document = add_document(documents, appointment, 'analysis', 'ЭКГ')
    assert get_document_by_id(documents, document.id) is document
    assert get_document_by_id(documents, 999) is None


def test_get_documents_by_appointment():
    app1 = _make_appointment(1)
    app2 = _make_appointment(2)
    documents = []
    add_document(documents, app1, 'analysis', 'Анализ 1')
    add_document(documents, app1, 'prescription', 'Рецепт 1')
    add_document(documents, app2, 'analysis', 'Анализ 2')

    assert len(get_documents_by_appointment(documents, app1)) == 2
    assert len(get_documents_by_appointment(documents, app2)) == 1


def test_get_documents_by_type():
    appointment = _make_appointment()
    documents = []
    add_document(documents, appointment, 'analysis', 'Анализ')
    add_document(documents, appointment, 'prescription', 'Рецепт')

    assert len(get_documents_by_type(documents, 'analysis')) == 1
    assert len(get_documents_by_type(documents, 'prescription')) == 1
    assert len(get_documents_by_type(documents, 'referral')) == 0


def test_delete_document():
    appointment = _make_appointment()
    documents = []
    document = add_document(documents, appointment, 'analysis', 'ЭКГ')
    assert delete_document(documents, document.id) is True
    assert len(documents) == 0
    assert delete_document(documents, 999) is False