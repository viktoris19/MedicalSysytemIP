from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.appointments import get_appointment_by_id
from storage import (
    load_appointments,
    load_patients,
    load_specialists,
)


def appointments(request: HttpRequest) -> HttpResponse:
    patients_list = load_patients('data/patients.json')
    specialists_list = load_specialists('data/specialists.json')
    appointments_list = load_appointments(
        'data/appointments.json',
        patients_list,
        specialists_list,
    )
    context = {'appointments': appointments_list}
    return render(
        request, 'appointments/appointment_list.html', context,
    )


def appointment_detail(
    request: HttpRequest, appointment_id: int,
) -> HttpResponse:
    patients_list = load_patients('data/patients.json')
    specialists_list = load_specialists('data/specialists.json')
    appointments_list = load_appointments(
        'data/appointments.json',
        patients_list,
        specialists_list,
    )
    appointment = get_appointment_by_id(
        appointments_list, appointment_id,
    )

    if appointment is None:
        return render(
            request,
            'appointments/appointment_not_found.html',
            status=404,
        )

    context = {'appointment': appointment}
    return render(
        request, 'appointments/appointment_detail.html', context,
    )