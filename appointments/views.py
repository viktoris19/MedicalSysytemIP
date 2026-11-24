from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Appointment
from .forms import AppointmentFilterForm, AppointmentForm, DocumentForm
from .mixins import DataMixin
from specialists.models import Specialist

class AppointmentListView(LoginRequiredMixin, DataMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 5 
    title = 'Записи на прием'
    
    def get_queryset(self):
        queryset = Appointment.objects.active().select_related('patient', 'specialist')
        
        form = AppointmentFilterForm(self.request.GET or None)
        if form.is_bound and form.is_valid():
            if form.cleaned_data.get('date'):
                queryset = queryset.filter(appointment_date=form.cleaned_data['date'])
            if form.cleaned_data.get('specialist'):
                queryset = queryset.filter(specialist=form.cleaned_data['specialist'])
                
        return queryset.order_by('-appointment_date', '-appointment_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AppointmentFilterForm(self.request.GET or None)
        return context

class AppointmentDetailView(LoginRequiredMixin, DataMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'
    pk_url_kwarg = 'appointment_id'
    title = 'Карточка приема'

class AppointmentCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')
    title = 'Создание приема'

    def form_valid(self, form):
        specialist = form.cleaned_data['specialist']
        date = form.cleaned_data['appointment_date']
        time = form.cleaned_data['appointment_time']
        
        is_busy = Appointment.objects.active().filter(
            specialist=specialist, appointment_date=date, appointment_time=time
        ).exists()
        
        if is_busy:
            form.add_error(None, "У этого врача уже есть прием на это время.")
            return self.form_invalid(form)
            
        return super().form_valid(form)

class AppointmentUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')
    pk_url_kwarg = 'appointment_id'
    title = 'Редактирование приема'

    def form_valid(self, form):
        specialist = form.cleaned_data['specialist']
        date = form.cleaned_data['appointment_date']
        time = form.cleaned_data['appointment_time']

        is_busy = Appointment.objects.active().filter(
            specialist=specialist, appointment_date=date, appointment_time=time
        ).exclude(pk=self.object.pk).exists()
        
        if is_busy:
            form.add_error(None, "У этого врача уже есть прием на это время.")
            return self.form_invalid(form)
            
        return super().form_valid(form)

@login_required
@require_POST
def appointment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = Appointment.Status.CANCELLED
    appointment.save()
    return redirect('appointments:list')

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