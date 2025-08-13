"""
Моделі, які впливають на розрахунок зарплати.
"""

from django.db import models
from solo.models import SingletonModel


class SalaryConfiguration(SingletonModel):
    """
    Модель для зберігання єдиного набору налаштувань зарплати.
    Використовує патерн Singleton з бібліотеки django-solo,
    що дозволяє створити лише один запис цієї моделі через адмін-панель.
    """
    # Базові ставки за замовчуванням для кожного рівня
    junior_base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=10000.0,
                                           verbose_name='Базова ставка Junior (грн)')
    middle_base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20000.0,
                                           verbose_name='Базова ставка Middle (грн)')
    senior_base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=35000.0,
                                           verbose_name='Базова ставка Senior (грн)')
    lead_base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=50000.0,
                                         verbose_name='Базова ставка Team Lead (грн)')

    # Коефіцієнти за замовчуванням для кожного рівня
    junior_coeff = models.DecimalField(max_digits=4, decimal_places=2, default=1.0, verbose_name='Коефіцієнт Junior')
    middle_coeff = models.DecimalField(max_digits=4, decimal_places=2, default=1.5, verbose_name='Коефіцієнт Middle')
    senior_coeff = models.DecimalField(max_digits=4, decimal_places=2, default=2.0, verbose_name='Коефіцієнт Senior')
    lead_coeff = models.DecimalField(max_digits=4, decimal_places=2, default=2.5, verbose_name='Коефіцієнт Team Lead')

    def __str__(self):
        return 'Глобальні налаштування зарплати'

    class Meta:
        verbose_name = 'Глобальні налаштування зарплати'


class TaskType(models.Model):
    """
    Стандартна модель для зберігання типів завдань та їхньої вартості.
    Це дозволяє динамічно додавати нові типи завдань через адмін-панель.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва типу завдання")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Вартість (грн)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип завдання"
        verbose_name_plural = "Типи завдань"
