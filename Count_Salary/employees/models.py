"""
Моделі для представлення даних про співробітників та їхні зарплатні записи.
"""
from django.db import models
from django.urls import reverse
from decimal import Decimal
from .services import SalaryCalculationService


class Employee(models.Model):
    """
    Модель "Співробітник". Зберігає основну інформацію про працівника.
    """
    LEVEL_CHOICES = [
        ('JUN', 'Junior'),
        ('MID', 'Middle'),
        ('SEN', 'Senior'),
        ('LEAD', 'Team Lead'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="По-батькові")
    level = models.CharField(max_length=4, choices=LEVEL_CHOICES, verbose_name="Рівень")

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Співробітник"
        verbose_name_plural = "Співробітники"


class SalaryRecord(models.Model):
    """
    Містить всю логіку, пов'язану з розрахунками.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_records',
                                 verbose_name="Співробітник")
    month = models.PositiveSmallIntegerField(verbose_name="Місяць (1-12)")
    year = models.PositiveSmallIntegerField(verbose_name="Рік (напр. 2025)")
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Фактично відпрацьовані години")
    standard_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Норма годин на місяць")
    tasks_completed_value = models.DecimalField(max_digits=10, decimal_places=2,
                                                verbose_name="Загальна вартість завдань (грн)")
    usd_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Курс USD на цей місяць")
    eur_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Курс EUR на цей місяць")
    # `editable=False` робить це поле невидимим у формах - воно розраховується автоматично.
    calculated_salary = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0.0,
                                            verbose_name="Розрахована зарплата (грн)")

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']  # Найновіші записи будуть першими
        verbose_name = "Запис про зарплату"
        verbose_name_plural = "Записи про зарплату"

    def __str__(self):
        return f"Зарплата для {self.employee.get_full_name()} за {self.month}.{self.year}"

    def save(self, *args, **kwargs):
        """
        Це ключовий елемент архітектури: перед кожним збереженням запису,
        викликається сервісний клас для автоматичного розрахунку зарплати.
        """
        service = SalaryCalculationService(salary_record=self)
        self.calculated_salary = service.calculate()
        super().save(*args, **kwargs)

    @property
    def overtime_hours(self):
        """Властивість, що динамічно розраховує понаднормові години."""
        overtime = self.actual_hours - self.standard_hours
        return max(overtime, Decimal(0))  # Повертає 0, якщо понаднормових не було

    @property
    def salary_in_usd(self):
        """Властивість, що динамічно розраховує зарплату в USD."""
        if self.usd_rate and self.usd_rate > 0:
            return self.calculated_salary / self.usd_rate
        return Decimal('0')

    @property
    def salary_in_eur(self):
        """Властивість, що динамічно розраховує зарплату в EUR."""
        if self.eur_rate and self.eur_rate > 0:
            return self.calculated_salary / self.eur_rate
        return Decimal('0')
