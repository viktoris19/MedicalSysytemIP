from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Appointment
from specialists.models import Specialist


def appointments(request):
    # Используем наш кастомный менеджер active()
    appointments_list = Appointment.objects.active().select_related('patient', 'specialist')
    
    # Фильтрация по статусу (если выбрано в GET)
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        appointments_list = appointments_list.filter(status=status_filter)
        
    appointments_list = appointments_list.order_by('-appointment_date', '-appointment_time')
    
    # Пагинация
    paginator = Paginator(appointments_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'appointments': page_obj,
        'selected_status': status_filter,
    }
    return render(request, 'appointments/appointment_list.html', context)

def statistics(request):
    # 1. Общая агрегация (демонстрация aggregate и Count)
    total_stats = Appointment.objects.aggregate(
        total=Count('id'),
        scheduled=Count('id', filter=Q(status=Appointment.Status.SCHEDULED)),
        completed=Count('id', filter=Q(status=Appointment.Status.COMPLETED)),
        cancelled=Count('id', filter=Q(status=Appointment.Status.CANCELLED)),
    )

    # 2. Группировка по статусам (демонстрация values + annotate)
    by_status = Appointment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    # Переводим технические статусы в красивые надписи
    status_dict = dict(Appointment.Status.choices)
    for item in by_status:
        item['status'] = status_dict.get(item['status'], item['status'])

    # 3. Статистика по специалистам (демонстрация annotate по обратной связи)
    by_specialist = Specialist.objects.annotate(
        appointments_count=Count('appointments')
    ).order_by('-appointments_count')

    context = {
        'total_stats': total_stats,
        'by_status': by_status,
        'by_specialist': by_specialist,
    }
    return render(request, 'appointments/statistics.html', context)