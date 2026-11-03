from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    insurance_policy = models.CharField(max_length=50, unique=True, verbose_name="Полис")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    
    # Новое поле для красивого URL
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name="URL-идентификатор"
    )

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def save(self, *args, **kwargs):
        # Если слаг не задан, генерируем его автоматически
        if not self.slug:
            # Формируем базовый слаг из фамилии и имени (транслитерация)
            base_slug = slugify(f"{self.last_name}-{self.first_name}")
            
            # Если после slugify осталась пустая строка, используем uuid
            if not base_slug:
                base_slug = f"patient-{uuid.uuid4().hex[:6]}"
            else:
                # Проверяем на уникальность
                if Patient.objects.filter(slug=base_slug).exists():
                    base_slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            
            self.slug = base_slug
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL карточки пациента для использования в шаблонах и админке"""
        return reverse('patients:detail', kwargs={'slug': self.slug})