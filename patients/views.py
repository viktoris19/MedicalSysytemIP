from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def patients(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, first_name, last_name, birth_date, insurance_policy
        FROM patients
        ORDER BY last_name
        """
    ).fetchall()
    conn.close()

    patients_list = [dict(row) for row in rows]
    return render(
        request,
        'patients/patient_list.html',
        {'patients': patients_list},
    )


def patient_detail(request: HttpRequest, patient_id: int) -> HttpResponse:
    conn = get_connection()

    patient_row = conn.execute(
        """
        SELECT id, first_name, last_name, birth_date,
               phone, email, insurance_policy, address
        FROM patients
        WHERE id = ?
        """,
        [patient_id],
    ).fetchone()

    if patient_row is None:
        conn.close()
        return render(
            request,
            'patients/patient_not_found.html',
            status=404,
        )

    appointments_rows = conn.execute(
        """
        SELECT
            appointments.id,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            specialists.first_name AS specialist_first_name,
            specialists.last_name AS specialist_last_name,
            specialists.speciality
        FROM appointments
        JOIN specialists ON appointments.specialist_id = specialists.id
        WHERE appointments.patient_id = ?
        ORDER BY appointments.appointment_date DESC
        """,
        [patient_id],
    ).fetchall()
    conn.close()

    context = {
        'patient': dict(patient_row),
        'appointments': [dict(row) for row in appointments_rows],
    }
    return render(request, 'patients/patient_detail.html', context)