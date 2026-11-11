from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Value
from django.db.models.functions import Concat
import uuid


class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    insurance_policy = models.CharField(max_length=50, unique=True, verbose_name="Полис")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL-идентификатор")

    # ВЫЧИСЛЯЕМОЕ ПОЛЕ (GeneratedField) - база склеивает имя и фамилию
    full_name = models.GeneratedField(
        expression=Concat('last_name', Value(' '), 'first_name'),
        output_field=models.CharField(max_length=205),
        db_persist=True,
        verbose_name="Полное имя"
    )

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.last_name}-{self.first_name}")
            if not base_slug:
                base_slug = f"patient-{uuid.uuid4().hex[:6]}"
            else:
                if Patient.objects.filter(slug=base_slug).exists():
                    base_slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('patients:detail', kwargs={'slug': self.slug})