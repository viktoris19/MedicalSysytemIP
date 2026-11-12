from django import forms
from django.utils import timezone
from .models import Appointment, Document
from specialists.models import Specialist

class AppointmentFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Дата приема",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    specialist = forms.ModelChoiceField(
        queryset=Specialist.objects.all(),
        required=False,
        label="Врач",
        empty_label="Все врачи",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'specialist', 'appointment_date', 'appointment_time', 'complaint', 'notes']
        labels = {
            'patient': 'Пациент',
            'specialist': 'Врач',
            'appointment_date': 'Дата приема',
            'appointment_time': 'Время приема',
            'complaint': 'Жалобы',
            'notes': 'Заметки',
        }
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'complaint': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'specialist': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_appointment_date(self):
        date = self.cleaned_data['appointment_date']
        if date < timezone.localdate():
            raise forms.ValidationError("Нельзя записаться на прием в прошлом.")
        return date

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }