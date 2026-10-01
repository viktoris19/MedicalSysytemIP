# Система управления медицинскими записями

## Назначение

Приложение для управления медицинскими записями пациентов,
специалистов и записей на приём.

Консольная версия (ПР3) дополнена веб-интерфейсом на Django (ПР5).

## Используемые технологии

- Python 3
- Django 5.2 — веб-фреймворк
- HTML — разметка (шаблоны Django)
- Bootstrap 5.3 — оформление
- pytest — тесты
- flake8 — проверка кода

## Страницы веб-интерфейса

| URL | View | Назначение |
|-----|------|-----------|
| `/` | `homepage.views.index` | Главная |
| `/patients/` | `patients.views.patients` | Список пациентов |
| `/patients/<int:patient_id>/` | `patients.views.patient_detail` | Карточка пациента |
| `/specialists/` | `specialists.views.specialists` | Список специалистов |
| `/specialists/<int:specialist_id>/` | `specialists.views.specialist_detail` | Карточка специалиста |
| `/appointments/` | `appointments.views.appointments` | Список записей |
| `/appointments/<int:appointment_id>/` | `appointments.views.appointment_detail` | Карточка записи |

## Запуск

### Веб-версия (Django)

```bash
python manage.py migrate
python manage.py runserver