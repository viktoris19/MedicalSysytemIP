from django.views.generic import ListView, DetailView
from appointments.mixins import DataMixin
from .models import Specialist

class SpecialistListView(DataMixin, ListView):
    model = Specialist
    template_name = 'specialists/specialist_list.html'
    context_object_name = 'specialists'
    paginate_by = 10
    title = 'Список специалистов'

    def get_queryset(self):
        return Specialist.objects.all().order_by('last_name')

class SpecialistDetailView(DataMixin, DetailView):
    model = Specialist
    template_name = 'specialists/specialist_detail.html'
    context_object_name = 'specialist'
    pk_url_kwarg = 'specialist_id'
    title = 'Карточка специалиста'