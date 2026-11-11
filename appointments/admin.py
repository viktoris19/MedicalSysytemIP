from django.contrib import admin
from .models import Appointment, Document

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'specialist', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'specialist')
    search_fields = ('id', 'patient__last_name', 'specialist__last_name')
    ordering = ('-appointment_date',)
    inlines = [DocumentInline]

    actions = ['mark_as_completed', 'mark_as_cancelled']

    @admin.action(description="Отметить как Завершенные")
    def mark_as_completed(self, request, queryset):
        queryset.update(status=Appointment.Status.COMPLETED)

    @admin.action(description="Отметить как Отмененные")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status=Appointment.Status.CANCELLED)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'appointment')