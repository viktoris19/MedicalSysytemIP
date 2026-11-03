from django.contrib import admin
from .models import Patient
from appointments.models import Appointment

# Связанные приемы прямо в карточке пациента
class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    fields = ('specialist', 'appointment_date', 'appointment_time', 'status')
    can_delete = False # Запрещаем удалять из карточки пациента

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'insurance_policy')
    search_fields = ('last_name', 'first_name', 'insurance_policy')
    list_filter = ('birth_date',)
    inlines = [AppointmentInline] # Подключаем таблицу