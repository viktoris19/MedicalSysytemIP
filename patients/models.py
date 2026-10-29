from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    insurance_policy = models.CharField(max_length=50, unique=True, verbose_name="Полис")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"