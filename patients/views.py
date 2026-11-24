from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Patient
from appointments.mixins import DataMixin
from django.contrib.auth.forms import UserCreationForm
from django.views import generic


class PatientListView(DataMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10  # Встроенная пагинация CBV
    title = 'Список пациентов'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) | Q(first_name__icontains=query)
            )
        return queryset.order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['total_count'] = self.get_queryset().count()
        return context

class PatientDetailView(DataMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'
    slug_url_kwarg = 'slug'
    title = 'Карточка пациента'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = self.object.appointments.select_related('specialist').order_by('-appointment_date')
        return context

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'