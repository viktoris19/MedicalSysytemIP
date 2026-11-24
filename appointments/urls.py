from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('create/', views.AppointmentCreateView.as_view(), name='create'),
    path('<int:appointment_id>/edit/', views.AppointmentUpdateView.as_view(), name='edit'),
    path('<int:appointment_id>/cancel/', views.appointment_cancel, name='cancel'),
    path('<int:appointment_id>/upload/', views.document_upload, name='document_upload'),
    path('<int:appointment_id>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('statistics/', views.statistics, name='statistics'),
]