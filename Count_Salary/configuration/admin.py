"""
Налаштування відображення моделей додатку 'configuration'
в стандартній адмін-панелі Django.
"""

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SalaryConfiguration, TaskType

# Це забезпечить, що в адмін-панелі буде лише один екземпляр налаштувань для редагування.
admin.site.register(SalaryConfiguration, SingletonModelAdmin)


admin.site.register(TaskType)   #дозволяє додавати/редагувати/видаляти типи завдань
