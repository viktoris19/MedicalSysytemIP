from django.contrib import admin
from .models import Appointment, Document

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'specialist', 'appointment_date', 'status')
    # Поиск по связанным таблицам (через __)
    search_fields = ('patient__last_name', 'specialist__last_name', 'id')
    list_filter = ('status', 'appointment_date', 'specialist')
    ordering = ('-appointment_date',)
    inlines = [DocumentInline]

    # Массовые действия (методичка требует)
    actions = ['mark_as_completed', 'mark_as_cancelled']

    @admin.action(description="Отметить как Завершенные")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.COMPLETED)
        self.message_user(request, f"{updated} приемов отмечено как завершенные.")

    @admin.action(description="Отметить как Отмененные")
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.CANCELLED)
        self.message_user(request, f"{updated} приемов отменено.")