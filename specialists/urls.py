from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('', views.specialists, name='list'),
    path('<str:specialist_id>/', views.specialist_detail, name='detail'),
]