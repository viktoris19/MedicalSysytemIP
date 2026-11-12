from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .models import Appointment, Document
from specialists.models import Specialist
from .forms import AppointmentFilterForm, AppointmentForm, DocumentForm

@login_required
def appointments(request):
    appointments_list = Appointment.objects.active().select_related('patient', 'specialist')
    
    form = AppointmentFilterForm(request.GET or None)
    if form.is_bound and form.is_valid():
        date = form.cleaned_data.get('date')
        specialist = form.cleaned_data.get('specialist')
        
        if date:
            appointments_list = appointments_list.filter(appointment_date=date)
        if specialist:
            appointments_list = appointments_list.filter(specialist=specialist)

    appointments_list = appointments_list.order_by('-appointment_date', '-appointment_time')
    
    paginator = Paginator(appointments_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'appointments/appointment_list.html', {
        'appointments': page_obj,
        'form': form,
    })

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            specialist = form.cleaned_data['specialist']
            date = form.cleaned_data['appointment_date']
            time = form.cleaned_data['appointment_time']
            
            is_busy = Appointment.objects.active().filter(
                specialist=specialist, 
                appointment_date=date, 
                appointment_time=time
            ).exists()

            if is_busy:
                form.add_error(None, "У этого врача уже есть прием на это время.")
            else:
                form.save()
                return redirect('appointments:list')
    else:
        form = AppointmentForm()
        
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_edit(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            specialist = form.cleaned_data['specialist']
            date = form.cleaned_data['appointment_date']
            time = form.cleaned_data['appointment_time']
            
            is_busy = Appointment.objects.active().filter(
                specialist=specialist, 
                appointment_date=date, 
                appointment_time=time
            ).exclude(pk=appointment.pk).exists()

            if is_busy:
                form.add_error(None, "У этого врача уже есть прием на это время.")
            else:
                form.save()
                return redirect('appointments:list')
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
@require_POST
def appointment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = Appointment.Status.CANCELLED
    appointment.save()
    return redirect('appointments:list')

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'specialist'),
        id=appointment_id
    )
    return render(
        request,
        'appointments/appointment_detail.html',
        {'appointment': appointment}
    )

@login_required
def statistics(request):
    total_stats = Appointment.objects.aggregate(
        total=Count('id'),
        scheduled=Count('id', filter=Q(status=Appointment.Status.SCHEDULED)),
        completed=Count('id', filter=Q(status=Appointment.Status.COMPLETED)),
        cancelled=Count('id', filter=Q(status=Appointment.Status.CANCELLED)),
    )

    by_status = Appointment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')

    status_dict = dict(Appointment.Status.choices)
    for item in by_status:
        item['status'] = status_dict.get(item['status'], item['status'])

    by_specialist = Specialist.objects.annotate(
        appointments_count=Count('appointments')
    ).order_by('-appointments_count')

    context = {
        'total_stats': total_stats,
        'by_status': by_status,
        'by_specialist': by_specialist,
    }
    return render(request, 'appointments/statistics.html', context)

@login_required
def document_upload(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES) 
        if form.is_valid():
            document = form.save(commit=False)
            document.appointment = appointment
            document.save()
            return redirect('appointments:detail', appointment_id=appointment.id)
    else:
        form = DocumentForm()
        
    return render(request, 'appointments/document_form.html', {'form': form, 'appointment': appointment})