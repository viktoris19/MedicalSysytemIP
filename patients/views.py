from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.patients import find_patient_by_id, sort_patients
from storage import (
    load_appointments,
    load_patients,
    load_specialists,
)

def patients(request: HttpRequest) -> HttpResponse:
    patients_list = load_patients('data/patients.json')
    context = {'patients': sort_patients(patients_list),}
    return render(request, 'patients/patient_list.html', context)

def patient_detail(request: HttpRequest, patient_id: int,) -> HttpResponse:
    patients_list = load_patients('data/patients.json')
    patient = find_patient_by_id(patients_list, patient_id)

    if patient is None:
        return render(
            request,
            'patients/patient_not_found.html',
            status=404,
        )

    specialists_list = load_specialists('data/specialists.json')
    appointments_list = load_appointments(
        'data/appointments.json',
        patients_list,
        specialists_list,
    )
    patient_appointments = [
        a for a in appointments_list if a.patient.id == patient.id
    ]

    context = {
        'patient': patient,
        'appointments': patient_appointments,
    }
    return render(request, 'patients/patient_detail.html', context)