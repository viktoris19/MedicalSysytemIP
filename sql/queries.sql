SELECT id, first_name, last_name, birth_date, insurance_policy
FROM patients
ORDER BY last_name;

SELECT id, first_name, last_name, speciality, experience_years
FROM specialists
ORDER BY last_name;

SELECT id, first_name, last_name, experience_years
FROM specialists
WHERE speciality = ?
ORDER BY experience_years DESC;

SELECT id, appointment_date, appointment_time, status
FROM appointments
WHERE patient_id = ?
  AND appointment_date BETWEEN ? AND ?
ORDER BY appointment_date DESC;

SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.status,
    appointments.complaint,
    appointments.diagnosis,
    patients.first_name AS patient_first_name,
    patients.last_name AS patient_last_name,
    patients.insurance_policy,
    specialists.first_name AS specialist_first_name,
    specialists.last_name AS specialist_last_name,
    specialists.speciality
FROM appointments
JOIN patients ON appointments.patient_id = patients.id
JOIN specialists ON appointments.specialist_id = specialists.id
WHERE appointments.id = ?;

SELECT
    appointments.id,
    appointments.appointment_date,
    appointments.appointment_time,
    patients.last_name AS patient_last_name,
    patients.first_name AS patient_first_name
FROM appointments
JOIN patients ON appointments.patient_id = patients.id
WHERE appointments.specialist_id = ?
  AND appointments.status = 'scheduled'
ORDER BY appointments.appointment_date;

SELECT COUNT(*) AS total_appointments
FROM appointments;

SELECT status, COUNT(*) AS count
FROM appointments
GROUP BY status
ORDER BY count DESC;

SELECT
    specialists.last_name,
    specialists.first_name,
    specialists.speciality,
    COUNT(appointments.id) AS appointments_count
FROM specialists
LEFT JOIN appointments ON specialists.id = appointments.specialist_id
GROUP BY specialists.id, specialists.last_name, specialists.first_name, specialists.speciality
ORDER BY appointments_count DESC;

SELECT
    specialists.last_name,
    specialists.first_name,
    COUNT(appointments.id) AS appointments_count
FROM specialists
JOIN appointments ON specialists.id = appointments.specialist_id
GROUP BY specialists.id, specialists.last_name, specialists.first_name
HAVING COUNT(appointments.id) > 1
ORDER BY appointments_count DESC;

SELECT id, last_name, first_name, speciality
FROM specialists
WHERE id NOT IN (
    SELECT specialist_id
    FROM appointments
    WHERE appointment_date = ?
      AND appointment_time = ?
      AND status != 'cancelled'
);

SELECT
    documents.id,
    documents.document_type,
    documents.title,
    documents.content,
    appointments.appointment_date
FROM documents
JOIN appointments ON documents.appointment_id = appointments.id
WHERE appointments.id = ?;