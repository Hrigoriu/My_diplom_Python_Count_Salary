"""
URL-маршрути для додатку 'widgets'.
"""
from django.urls import path
from . import views

# app_name дозволяє створювати простір імен для URL-адрес.

app_name = 'widgets'

urlpatterns = [
    # Єдиний маршрут, який обробляє API-запити для погоди від фронтенду.
    # Наприклад: /widgets/api/weather/?city=Lviv
    path('api/weather/', views.weather_api, name='weather-api'),
]