from django.urls import path

from . import views

urlpatterns = [
    path('', views.specialists, name='specialists'),
    path(
        '<int:specialist_id>/',
        views.specialist_detail,
        name='specialist_detail',
    ),
]