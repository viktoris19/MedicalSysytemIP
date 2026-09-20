import os
import tempfile

from models import Appointment, Document, Patient, Specialist
import storage


def test_save_and_load_patients():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, 'patients.json')
        patients = [Patient(
            1, 'Иван', 'Смирнов', '1985-06-15',
            '+79990000000', 'ivan@mail.ru', 'POLICY-1',
        )]
        assert storage.save_patients(filename, patients) is True

        loaded = storage.load_patients(filename)
        assert len(loaded) == 1
        assert loaded[0].first_name == 'Иван'
        assert loaded[0].insurance_policy == 'POLICY-1'


def test_save_and_load_specialists():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, 'specialists.json')
        specialists = [Specialist(
            1, 'Анна', 'Петрова', 'Кардиолог',
            '+79991234567', 'petrova@clinic.ru', 10,
        )]
        assert storage.save_specialists(filename, specialists) is True

        loaded = storage.load_specialists(filename)
        assert len(loaded) == 1
        assert loaded[0].speciality == 'Кардиолог'


def test_save_and_load_appointments():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, 'appointments.json')
        patient = Patient(
            1, 'Иван', 'Смирнов', '1985-06-15',
            '+79990000000', 'ivan@mail.ru', 'POLICY-1',
        )
        specialist = Specialist(
            1, 'Анна', 'Петрова', 'Кардиолог',
            '+79991234567', 'petrova@clinic.ru', 10,
        )
        appointments = [Appointment(
            1, patient, specialist, '2026-09-25', '10:30',
        )]
        assert storage.save_appointments(filename, appointments) is True

        loaded = storage.load_appointments(
            filename, [patient], [specialist],
        )
        assert len(loaded) == 1
        assert loaded[0].patient.id == 1
        assert loaded[0].specialist.id == 1


def test_save_and_load_documents():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, 'documents.json')
        patient = Patient(
            1, 'Иван', 'Смирнов', '1985-06-15',
            '+79990000000', 'ivan@mail.ru', 'POLICY-1',
        )
        specialist = Specialist(
            1, 'Анна', 'Петрова', 'Кардиолог',
            '+79991234567', 'petrova@clinic.ru', 10,
        )
        appointment = Appointment(
            1, patient, specialist, '2026-09-25', '10:30',
        )
        documents = [Document(
            1, appointment, 'analysis', 'ЭКГ', content='текст',
        )]
        assert storage.save_documents(filename, documents) is True

        loaded = storage.load_documents(filename, [appointment])
        assert len(loaded) == 1
        assert loaded[0].title == 'ЭКГ'


def test_load_missing_file_returns_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, 'missing.json')
        assert storage.load_patients(filename) == []