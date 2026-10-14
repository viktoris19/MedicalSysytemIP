from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointments, name='list'),
    path('statistics/', views.statistics, name='statistics'),
    path('<str:appointment_id>/', views.appointment_detail, name='detail'),
]