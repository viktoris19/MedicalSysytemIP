from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('', views.SpecialistListView.as_view(), name='list'),
    path('<int:specialist_id>/', views.SpecialistDetailView.as_view(), name='detail'),
]