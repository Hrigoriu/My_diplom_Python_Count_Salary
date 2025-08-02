"""
Ізолює всю логіку взаємодії з зовнішніми API.
"""
import requests
from django.conf import settings


class WeatherService:
    """
    Клас-сервіс для отримання даних про погоду з API OpenWeatherMap.
    """
    # Зчитуємо API-ключ з налаштувань Django (settings.py).
    # `getattr` використовується для безпечного доступу: якщо ключ не знайдено,
    # він не викличе помилку, а просто поверне None.
    API_KEY = getattr(settings, 'OPENWEATHER_API_KEY', None)
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> dict:
        """
        Виконує запит до API та повертає дані про погоду у вигляді словника.
        Повертає словник з даними або з інформацією про помилку.
        """
        # 1. Перевірка наявності ключа
        if not self.API_KEY or self.API_KEY == "1ce0dddc46bf4bd643ca7ac5f18f7f42":
            return {"error": "API-ключ для погоди не налаштовано."}

        # 2. Формування параметрів запиту
        params = {
            "q": city,
            "appid": self.API_KEY,
            "units": "metric",  # Отримуємо температуру в градусах Цельсія
            "lang": "uk",  # Мова відповіді - українська
        }

        # 3. Виконання запиту з обробкою можливих помилок
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)  # timeout - щоб не чекати вічно
            response.raise_for_status()
            data = response.json()

            # 4. Формування успішної відповіді лише з потрібними даними
            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "city": data["name"],
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {"error": "Неправильний API-ключ."}
            if e.response.status_code == 404:
                return {"error": f"Місто '{city}' не знайдено."}
            return {"error": f"Помилка сервера погоди: {e.response.status_code}"}
        except requests.exceptions.RequestException:
            return {"error": "Не вдалося з'єднатися з сервісом погоди."}
        except (KeyError, IndexError):
            return {"error": "Отримано некоректну відповідь від сервісу погоди."}