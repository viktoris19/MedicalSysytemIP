from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Appointment
from specialists.models import Specialist
from django.core.paginator import Paginator

def appointments(request: HttpRequest) -> HttpResponse:
    appointments_list = Appointment.objects.select_related('patient', 'specialist')

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        appointments_list = appointments_list.filter(status=status_filter)
    appointments_list = appointments_list.exclude(status='cancelled')
    
    appointments_list = appointments_list.order_by('-appointment_date', '-appointment_time')
    
    paginator = Paginator(appointments_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'appointments': page_obj,
        'selected_status': status_filter,
    }
    return render(request, 'appointments/appointment_list.html', context)

def appointment_detail(request: HttpRequest, appointment_id: int) -> HttpResponse:
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'specialist'),
        id=appointment_id
    )
    return render(
        request,
        'appointments/appointment_detail.html',
        {'appointment': appointment},
    )

def statistics(request: HttpRequest) -> HttpResponse:
    # 1. Аналог GROUP BY status
    by_status = Appointment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    # 2. Аналог LEFT JOIN + COUNT
    by_specialist = Specialist.objects.annotate(
        appointments_count=Count('appointments')
    ).order_by('-appointments_count')

    context = {
        'by_status': by_status,
        'by_specialist': by_specialist,
    }
    return render(request, 'appointments/statistics.html', context)