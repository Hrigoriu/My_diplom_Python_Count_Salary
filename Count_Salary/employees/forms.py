"""
Форми Django для зручної роботи з даними моделей в шаблонах.
"""

from django import forms
from .models import Employee, SalaryRecord

class EmployeeForm(forms.ModelForm):
    """Форма для створення та редагування даних співробітника."""
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'patronymic', 'level']


class SalaryRecordForm(forms.ModelForm):
    """Форма для створення та редагування запису про зарплату."""
    class Meta:
        model = SalaryRecord
        # Вказуємо поля, які користувач може заповнювати.
        # 'employee' заповнюється автоматично у view,
        # 'calculated_salary' - у методі .save() моделі.
        fields = [
            'month', 'year', 'actual_hours', 'standard_hours',
            'tasks_completed_value', 'usd_rate', 'eur_rate'
        ]