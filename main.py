from datetime import date

patient_first_name = "Иван"
patient_last_name = "Смирнов"
patient_birth_year = 1985
patient_age = 2026 - patient_birth_year  
patient_phone = "+79999876543"
patient_insurance = "POLICY-12345"

patient_age_str = str(patient_age)

doctor_first_name = "Анна"
doctor_last_name = "Петрова"
doctor_speciality = "Кардиолог"
doctor_experience = 15

if doctor_experience >= 10:
    doctor_experience_level = "Опытный специалист"
elif doctor_experience >= 5:
    doctor_experience_level = "Специалист со стажем"
else:
    doctor_experience_level = "Молодой специалист"

appointment_date = date(2026, 9, 25)
appointment_time = "10:30"
is_slot_available = True

patient_full_name = patient_last_name + " " + patient_first_name
doctor_full_name = doctor_last_name + " " + doctor_first_name
availability_text = str(is_slot_available)
experience_text = str(doctor_experience) + " лет"

def get_appointment_status(is_available):
    if is_available:
        return "Доступна для записи"
    else:
        return "Занята (запись невозможна)"

print("=" * 55)
print("СИСТЕМА УПРАВЛЕНИЯ МЕДИЦИНСКИМИ ЗАПИСЯМИ")
print("=" * 55)

print("\n--- ИНФОРМАЦИЯ О ПАЦИЕНТЕ ---")
print("ФИО: " + patient_full_name)
print("Год рождения: " + str(patient_birth_year))
print("Возраст: " + patient_age_str + " лет")
print("Телефон: " + patient_phone)
print("Номер полиса: " + patient_insurance)

print("\n--- ИНФОРМАЦИЯ О ВРАЧЕ ---")
print("ФИО: " + doctor_full_name)
print("Специальность: " + doctor_speciality)
print("Стаж: " + experience_text)
print("Уровень: " + doctor_experience_level)

print("\n--- ИНФОРМАЦИЯ О ЗАПИСИ ---")
print("Дата приема: " + appointment_date.strftime("%d.%m.%Y"))
print("Время приема: " + appointment_time)
print("Доступность слота: " + availability_text)

print("\n--- РЕЗУЛЬТАТ ПРОВЕРКИ ---")

status = get_appointment_status(is_slot_available)
print("Статус записи: " + status)

if is_slot_available and patient_age >= 18:
    print("Запись возможна: пациент совершеннолетний, слот свободен")
elif is_slot_available and patient_age < 18:
    print("Запись требует согласия родителей")
else:
    print("Запись невозможна: слот занят")

if patient_age < 18:
    age_category = "Ребенок"
elif patient_age < 60:
    age_category = "Взрослый"
else:
    age_category = "Пожилой"

print("Возрастная категория пациента: " + age_category)

print("\n" + "=" * 55)
print("ИНФОРМАЦИЯ ДЛЯ АДМИНИСТРАТОРА")
print("=" * 55)

is_patient_adult = patient_age >= 18
is_doctor_experienced = doctor_experience >= 5

can_book = is_slot_available and is_patient_adult

print("Пациент совершеннолетний: " + str(is_patient_adult))
print("Врач имеет стаж более 5 лет: " + str(is_doctor_experienced))
print("Возможность записи (с учетом возраста): " + str(can_book))

if can_book:
    print(">>> РЕКОМЕНДАЦИЯ: Запись подтверждена")
else:
    print(">>> РЕКОМЕНДАЦИЯ: Запись отклонена (причина - слот занят или пациент несовершеннолетний)")

print("=" * 55)