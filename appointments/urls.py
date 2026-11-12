from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointments, name='list'),
    path('statistics/', views.statistics, name='statistics'),
    path('create/', views.appointment_create, name='create'),
    path('<int:appointment_id>/edit/', views.appointment_edit, name='edit'),
    path('<int:appointment_id>/cancel/', views.appointment_cancel, name='cancel'),
    path('<int:appointment_id>/upload/', views.document_upload, name='document_upload'),
    path('<int:appointment_id>/', views.appointment_detail, name='detail'),
]