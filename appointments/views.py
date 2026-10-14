from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def appointments(request: HttpRequest) -> HttpResponse:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT
            appointments.id,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            patients.last_name AS patient_last_name,
            patients.first_name AS patient_first_name,
            specialists.last_name AS specialist_last_name,
            specialists.first_name AS specialist_first_name,
            specialists.speciality
        FROM appointments
        JOIN patients ON appointments.patient_id = patients.id
        JOIN specialists ON appointments.specialist_id = specialists.id
        ORDER BY appointments.appointment_date DESC
        """
    ).fetchall()
    conn.close()

    return render(
        request,
        'appointments/appointment_list.html',
        {'appointments': [dict(row) for row in rows]},
    )


def appointment_detail(
    request: HttpRequest, appointment_id: int,
) -> HttpResponse:
    conn = get_connection()
    row = conn.execute(
        """
        SELECT
            appointments.id,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            appointments.complaint,
            appointments.diagnosis,
            appointments.notes,
            patients.id AS patient_id,
            patients.first_name AS patient_first_name,
            patients.last_name AS patient_last_name,
            specialists.id AS specialist_id,
            specialists.first_name AS specialist_first_name,
            specialists.last_name AS specialist_last_name,
            specialists.speciality
        FROM appointments
        JOIN patients ON appointments.patient_id = patients.id
        JOIN specialists ON appointments.specialist_id = specialists.id
        WHERE appointments.id = ?
        """,
        [appointment_id],
    ).fetchone()
    conn.close()

    if row is None:
        return render(
            request,
            'appointments/appointment_not_found.html',
            status=404,
        )

    return render(
        request,
        'appointments/appointment_detail.html',
        {'appointment': dict(row)},
    )


def statistics(request: HttpRequest) -> HttpResponse:
    conn = get_connection()

    by_status = conn.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM appointments
        GROUP BY status
        ORDER BY count DESC
        """
    ).fetchall()

    by_specialist = conn.execute(
        """
        SELECT
            specialists.last_name,
            specialists.first_name,
            specialists.speciality,
            COUNT(appointments.id) AS appointments_count
        FROM specialists
        LEFT JOIN appointments
            ON specialists.id = appointments.specialist_id
        GROUP BY specialists.id, specialists.last_name,
                 specialists.first_name, specialists.speciality
        ORDER BY appointments_count DESC
        """
    ).fetchall()
    conn.close()

    context = {
        'by_status': [dict(row) for row in by_status],
        'by_specialist': [dict(row) for row in by_specialist],
    }
    return render(request, 'appointments/statistics.html', context)