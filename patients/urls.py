from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.PatientListView.as_view(), name='list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<slug:slug>/', views.PatientDetailView.as_view(), name='detail'),
]