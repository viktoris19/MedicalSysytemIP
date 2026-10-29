from django.db import models
from patients.models import Patient
from specialists.models import Specialist

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments", verbose_name="Пациент")
    specialist = models.ForeignKey(Specialist, on_delete=models.PROTECT, related_name="appointments", verbose_name="Специалист")
    appointment_date = models.DateField(verbose_name="Дата приема")
    appointment_time = models.TimeField(verbose_name="Время приема")
    status = models.CharField(max_length=50, default='scheduled', verbose_name="Статус")
    complaint = models.TextField(blank=True, null=True, verbose_name="Жалобы")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Диагноз")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self):
        return f"Прием {self.patient} у {self.specialist} ({self.appointment_date})"

class Document(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="documents", verbose_name="Прием")
    document_type = models.CharField(max_length=50, verbose_name="Тип документа")
    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(blank=True, null=True, verbose_name="Содержимое")
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Путь к файлу")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title