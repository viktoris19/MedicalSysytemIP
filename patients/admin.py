from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'insurance_policy')
    search_fields = ('last_name', 'first_name', 'insurance_policy')
    list_filter = ('birth_date',)