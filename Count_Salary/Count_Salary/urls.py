"""
URL configuration for Count_Salary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employees import views as employee_views

urlpatterns = [
    path('admin/', admin.site.urls),                # Шлях до стандартної адмін-панелі Django
    path('', employee_views.home, name='home'),     # Головна сторінка сайту (http://127.0.0.1:8000/)
    path('employees/', include('employees.urls')),  # Всі URL, з /employees/, будуть оброблятися в файлі employees/urls.py
    path('reports/', include('reports.urls')),      # Всі URL, з /reports/, будуть оброблятися в файлі reports/urls.py
    path('configuration/', include('configuration.urls')),  # Всі URL, з /configuration/, будуть оброблятися в файлі reports/configuration.py
    path('widgets/', include('widgets.urls')),      # Всі URL, з /widgets/, будуть оброблятися в файлі widgets/urls.py
]