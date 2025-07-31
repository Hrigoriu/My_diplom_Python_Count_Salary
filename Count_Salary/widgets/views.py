from django.shortcuts import render

"""
Views для додатку 'widgets', які виступають у ролі API-ендпоінтів.
"""
from django.http import JsonResponse
from .services import WeatherService


def weather_api(request):
    """
    API-ендпоінт, який приймає місто з GET-параметрів,
    викликає сервіс для отримання даних про погоду та повертає результат у форматі JSON.
    """
    # Отримуємо назву міста з параметрів URL (?city=...),
    # якщо її не передано, за замовчуванням використовуємо "Київ".
    city = request.GET.get('city', 'Київ')

    # Створюємо екземпляр нашого сервісу
    weather_service = WeatherService()
    weather_data = weather_service.get_weather(city)

    # Якщо сервіс повернув помилку, передаємо її клієнту
    # з відповідним HTTP-статусом, щоб JavaScript міг це обробити.
    if 'error' in weather_data:
        return JsonResponse(weather_data, status=400)

    # Якщо все успішно, повертаємо дані у форматі JSON
    return JsonResponse(weather_data)
