from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patients, name='list'),
    path('<slug:slug>/', views.patient_detail, name='detail'),
]