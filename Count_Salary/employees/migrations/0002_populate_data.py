from django.db import migrations
import random
from decimal import Decimal

# Списки даних для генерації реалістичних імен
FIRST_NAMES = ["Олександр", "Андрій", "Дмитро", "Сергій", "Микола", "Іван", "Анна", "Олена", "Тетяна", "Марія",
               "Наталія", "Світлана"]
LAST_NAMES = ["Шевченко", "Коваленко", "Бондаренко", "Ткаченко", "Петренко", "Іванов", "Захарченко", "Павленко",
              "Сидоренко", "Кравченко"]
PATRONYMICS = ["Олександрович", "Андрійович", "Дмитрович", "Сергійович", "Іванович", "Олександрівна", "Андріївна",
               "Дмитрівна", "Сергіївна"]
LEVELS = ['JUN', 'MID', 'SEN', 'LEAD']


def populate_employees_and_salaries(apps, schema_editor):
    """
    Фінальна, надійна версія скрипту, яка розраховує зарплату всередині міграції.
    """
    # Отримує доступ до "історичних" версій моделей
    Employee = apps.get_model('employees', 'Employee')
    SalaryRecord = apps.get_model('employees', 'SalaryRecord')
    SalaryConfiguration = apps.get_model('configuration', 'SalaryConfiguration')

    # Очищує таблицю співробітників для чистого запуску
    Employee.objects.all().delete()

    # --- Завантажує налаштування (ставки і коефіцієнти), які вже мають існувати в базі ---
    try:
        config = SalaryConfiguration.objects.get()
    except SalaryConfiguration.DoesNotExist:
        raise Exception("Помилка! Міграція для створення конфігурації не була застосована. Запустіть 'migrate' знову.")

    # Готує словник з налаштуваннями для швидкого доступу
    level_map = {
        'JUN': (config.junior_base_rate, config.junior_coeff),
        'MID': (config.middle_base_rate, config.middle_coeff),
        'SEN': (config.senior_base_rate, config.senior_coeff),
        'LEAD': (config.lead_base_rate, config.lead_coeff),
    }

    print("\n[Employees] Налаштування зарплат завантажено. Починаємо створювати співробітників...")

    employees = []
    for _ in range(20):
        employee = Employee.objects.create(
            first_name=random.choice(FIRST_NAMES),
            last_name=random.choice(LAST_NAMES),
            patronymic=random.choice(PATRONYMICS),
            level=random.choice(LEVELS),
        )
        employees.append(employee)

    records_to_bulk_create = []
    for employee in employees:
        current_usd_rate = Decimal(random.uniform(39.5, 42.0)).quantize(Decimal("0.01"))
        current_eur_rate = Decimal(random.uniform(43.0, 45.5)).quantize(Decimal("0.01"))
        base_rate, coefficient = level_map.get(employee.level)

        for i in range(24):
            year, month = 2023 + (i // 12), 1 + (i % 12)
            standard_hours = Decimal('160.00')
            actual_hours = standard_hours + Decimal(random.uniform(-10.0, 15.0)).quantize(Decimal("0.01"))
            tasks_value = Decimal(random.uniform(5000, 25000)).quantize(Decimal("0.01"))

            # --- ЯВНИЙ РОЗРАХУНОК ЗАРПЛАТИ (логіка з SalaryCalculationService) ---
            hourly_part = (base_rate * actual_hours) / standard_hours if standard_hours > 0 else Decimal('0')
            final_hourly_part = hourly_part * coefficient
            final_salary = (final_hourly_part + tasks_value).quantize(Decimal('0.01'))
            # --- Кінець розрахунку ---

            record = SalaryRecord(
                employee=employee, month=month, year=year,
                actual_hours=actual_hours, standard_hours=standard_hours,
                tasks_completed_value=tasks_value, usd_rate=current_usd_rate, eur_rate=current_eur_rate,
                calculated_salary=final_salary  # <--- Вставляємо вже розраховану зарплату
            )
            records_to_bulk_create.append(record)

            current_usd_rate += Decimal(random.uniform(-0.5, 0.5)).quantize(Decimal("0.01"))
            current_eur_rate += Decimal(random.uniform(-0.5, 0.5)).quantize(Decimal("0.01"))

    # Створює всі 480 записів одним швидким запитом!
    SalaryRecord.objects.bulk_create(records_to_bulk_create)
    print(f"[Employees] Створено та розраховано зарплати для {len(records_to_bulk_create)} записів.")


class Migration(migrations.Migration):
    # ВАЖЛИВО: Ця міграція залежить як від створення таблиць 'employees',
    # так і від міграції, що створює конфігурацію. Це гарантує правильний порядок виконання.
    dependencies = [
        ('employees', '0001_initial'),
        ('configuration', '0002_create_default_config'),
    ]
    operations = [
        migrations.RunPython(populate_employees_and_salaries),
    ]