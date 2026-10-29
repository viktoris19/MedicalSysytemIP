from django.contrib import admin
from .models import Appointment, Document

# Вспомогательный класс, чтобы документы можно было добавлять прямо в карточке приема
class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # В списке показываем пациента, врача и дату
    list_display = ('id', 'patient', 'specialist', 'appointment_date', 'status')
    # Фильтры справа
    list_filter = ('status', 'appointment_date', 'specialist')
    # Поиск по ID или ФИО пациента (через двойное подчеркивание)
    search_fields = ('id', 'patient__last_name', 'specialist__last_name')
    # Добавляем документы прямо внутрь формы приема
    inlines = [DocumentInline]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'appointment')
    list_filter = ('document_type',)
    search_fields = ('title', 'content')