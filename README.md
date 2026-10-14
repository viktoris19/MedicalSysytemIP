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

## Шаблоны Django (ПР6)

Веб-интерфейс переведён на Django Templates:
- базовый шаблон `templates/base.html`;
- наследование через `{% extends %}`;
- включаемые шаблоны `{% include %}`;
- передача данных через контекст;
- циклы `{% for %}` и условия `{% if %}`;
- именованные URL и namespaces;
- фильтры `|length`, `|default`;
- собственные статические файлы: CSS, JS, изображение.

HTML больше не формируется в Python-коде view-функций.
Функция `page()` удалена.

## Запуск

### Веб-версия (Django)

```bash
python manage.py migrate
python manage.py runserver

## База данных (ПР7)

### Таблицы

| Таблица | Назначение |
|---------|-----------|
| `patients` | Пациенты медицинского центра |
| `specialists` | Врачи-специалисты |
| `appointments` | Записи на приём |
| `documents` | Медицинские документы |

### Связи

- `appointments.patient_id → patients.id`
- `appointments.specialist_id → specialists.id`
- `documents.appointment_id → appointments.id`

### Файлы проекта

- `sql/schema.sql` — создание таблиц;
- `sql/queries.sql` — 12 SQL-запросов;
- `db/database.py` — подключение к SQLite;
- `db/import_json.py` — импорт данных из JSON;
- `data/medical_records.sqlite` — файл базы данных.

### Запуск

```bash
python -m db.import_json    # импорт данных из JSON (один раз)
python manage.py runserver  # запуск веб-приложения