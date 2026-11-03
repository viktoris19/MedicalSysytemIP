from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <-- Добавить

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('patients/', include('patients.urls')),
    path('specialists/', include('specialists.urls')),
    path('appointments/', include('appointments.urls')),
]

# <-- Добавить блок для Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns