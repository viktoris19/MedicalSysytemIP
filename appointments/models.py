from django.db import models
from patients.models import Patient
from specialists.models import Specialist
from django.utils import timezone

# 1. Создаем собственный QuerySet (как требует ПР10)
class AppointmentQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Appointment.Status.SCHEDULED)
    
    def completed(self):
        return self.filter(status=Appointment.Status.COMPLETED)
    
    def cancelled(self):
        return self.filter(status=Appointment.Status.CANCELLED)

    def for_date(self, date):
        return self.filter(appointment_date=date)


class Appointment(models.Model):
    # 2. Создаем TextChoices для статусов
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Запланировано'
        COMPLETED = 'completed', 'Завершено'
        CANCELLED = 'cancelled', 'Отменено'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments", verbose_name="Пациент")
    specialist = models.ForeignKey(Specialist, on_delete=models.PROTECT, related_name="appointments", verbose_name="Специалист")
    appointment_date = models.DateField(verbose_name="Дата приема")
    appointment_time = models.TimeField(verbose_name="Время приема")
    
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.SCHEDULED, 
        verbose_name="Статус"
    )
    complaint = models.TextField(blank=True, null=True, verbose_name="Жалобы")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Диагноз")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")

    # 3. Подключаем кастомный менеджер
    objects = AppointmentQuerySet.as_manager()

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self):
        return f"Прием {self.patient} у {self.specialist} ({self.appointment_date})"

# 4. Модель Документов (чтобы не было ошибки импорта)
class Document(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title