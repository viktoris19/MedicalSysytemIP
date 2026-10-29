from django.contrib import admin
from .models import Specialist

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'speciality', 'experience_years')
    search_fields = ('last_name', 'first_name', 'speciality')
    list_filter = ('speciality',)