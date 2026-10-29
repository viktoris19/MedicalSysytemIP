from django.db import models

class Specialist(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    speciality = models.CharField(max_length=100, verbose_name="Специальность")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Стаж (лет)")

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.speciality})"