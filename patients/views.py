from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Patient

def patients(request: HttpRequest) -> HttpResponse:
    # Получаем всех пациентов
    patients_list = Patient.objects.all().order_by('last_name')
    
    # Поиск по фамилии или имени
    query = request.GET.get('q', '').strip()
    if query:
        patients_list = patients_list.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query)
        )
    
    # Пагинация
    paginator = Paginator(patients_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'patients': page_obj,
        'total_count': patients_list.count(),
        'search_query': query,
    }
    return render(request, 'patients/patient_list.html', context)


def patient_detail(request: HttpRequest, patient_id: int) -> HttpResponse:
    # Получаем пациента по ID (если нет — вернется 404)
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Получаем записи на прием для этого пациента
    appointments = patient.appointments.select_related('specialist').order_by('-appointment_date')

    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patients/patient_detail.html', context)