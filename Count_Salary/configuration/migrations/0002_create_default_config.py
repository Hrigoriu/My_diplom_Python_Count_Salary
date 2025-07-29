from django.db import migrations


def create_default_configuration(apps, schema_editor):
    SalaryConfiguration = apps.get_model('configuration', 'SalaryConfiguration')
    TaskType = apps.get_model('configuration', 'TaskType')

    # Створює єдиний екземпляр налаштувань, якщо він ще не існує.
    # Значення для полів (10000.0, 1.0 і т.д.) будуть взяті з `default`
    # параметрів, які ми визначили в models.py.
    SalaryConfiguration.objects.get_or_create()

    print("\n[Configuration] Створено екземпляр конфігурації за замовчуванням.")

    # Створює базові типи завдань
    TaskType.objects.get_or_create(name='Simple', defaults={'cost': 100.00})
    TaskType.objects.get_or_create(name='Medium', defaults={'cost': 250.00})
    TaskType.objects.get_or_create(name='Complex', defaults={'cost': 500.00})

    print("[Configuration] Створено базові типи завдань.")


class Migration(migrations.Migration):
    # Ця міграція повинна виконуватися після початкової міграції, яка створює таблиці
    dependencies = [
        ('configuration', '0001_initial'),
    ]

    # Вказуємо Django виконати нашу функцію
    operations = [
        migrations.RunPython(create_default_configuration),
    ]