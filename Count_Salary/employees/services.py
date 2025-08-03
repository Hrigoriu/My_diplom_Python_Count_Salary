"""
Сервісний шар для інкапсуляції бізнес-логіки.
"""
from decimal import Decimal
from configuration.models import SalaryConfiguration


class SalaryCalculationService:
    """
    Інкапсулює складну логіку розрахунку зарплати.
    Має єдину відповідальність: взяти дані і повернути результат.
    """

    def __init__(self, salary_record):
        self.record = salary_record
        self.employee = salary_record.employee
        try:
            self.config = SalaryConfiguration.get_solo()
        except SalaryConfiguration.DoesNotExist:
            raise ValueError("Глобальні налаштування зарплати не знайдено! Створіть їх в адмін-панелі.")

    def _get_base_rate_and_coeff(self):
        """Приватний метод для отримання ставки та коефіцієнта залежно від рівня."""
        level_map = {
            'JUN': (self.config.junior_base_rate, self.config.junior_coeff),
            'MID': (self.config.middle_base_rate, self.config.middle_coeff),
            'SEN': (self.config.senior_base_rate, self.config.senior_coeff),
            'LEAD': (self.config.lead_base_rate, self.config.lead_coeff),
        }
        return level_map.get(self.employee.level, (Decimal('0'), Decimal('1')))

    def calculate(self) -> Decimal:
        """
        Головний метод, що виконує розрахунок за фінальною, виправленою формулою:
        Зарплата = ( (Базова ставка * Факт. години) / Норма годин ) * Коефіцієнт + Вартість завдань.
        """
        base_rate, coefficient = self._get_base_rate_and_coeff()

        if self.record.standard_hours and self.record.standard_hours > 0:
            hourly_part = (base_rate * self.record.actual_hours) / self.record.standard_hours
        else:
            hourly_part = Decimal('0')

        final_hourly_part = hourly_part * coefficient
        final_salary = final_hourly_part + self.record.tasks_completed_value

        return final_salary.quantize(Decimal('0.01'))