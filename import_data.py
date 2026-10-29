import os
import django
import sqlite3
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medrec.settings')
django.setup()

from patients.models import Patient
from specialists.models import Specialist
from appointments.models import Appointment, Document

conn = sqlite3.connect('data/medical_records.sqlite')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("Начинаем перенос...")

for row in cur.execute("SELECT * FROM patients").fetchall():
    Patient.objects.update_or_create(
        id=row['id'],
        defaults={
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'birth_date': row['birth_date'],
            'phone': row['phone'],
            'email': row['email'],
            'insurance_policy': row['insurance_policy'],
            'address': row['address']
        }
    )
print("Пациенты перенесены.")

for row in cur.execute("SELECT * FROM specialists").fetchall():
    Specialist.objects.update_or_create(
        id=row['id'],
        defaults={
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'speciality': row['speciality'],
            'phone': row['phone'],
            'email': row['email'],
            'experience_years': row['experience_years']
        }
    )
print("Специалисты перенесены.")

for row in cur.execute("SELECT * FROM appointments").fetchall():
    Appointment.objects.update_or_create(
        id=row['id'],
        defaults={
            'patient_id': row['patient_id'],
            'specialist_id': row['specialist_id'],
            'appointment_date': row['appointment_date'],
            'appointment_time': row['appointment_time'],
            'status': row['status'],
            'complaint': row['complaint'],
            'diagnosis': row['diagnosis'],
            'notes': row['notes']
        }
    )
print("Приемы перенесены.")

for row in cur.execute("SELECT * FROM documents").fetchall():
    Document.objects.update_or_create(
        id=row['id'],
        defaults={
            'appointment_id': row['appointment_id'],
            'document_type': row['document_type'],
            'title': row['title'],
            'content': row['content'],
            'file_path': row['file_path']
        }
    )
print("Документы перенесены.")

conn.close()
print("Все данные успешно перенесены!")