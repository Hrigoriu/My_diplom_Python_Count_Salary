from django.db import migrations


def create_default_configuration(apps, schema_editor):
    """
    Ця функція запускається під час міграції і створює
    початкові, базові налаштування, щоб проєкт міг працювати відразу.
    """

    SalaryConfiguration = apps.get_model('configuration', 'SalaryConfiguration')
    TaskType = apps.get_model('configuration', 'TaskType')

    # Створює єдиний екземпляр налаштувань.
    SalaryConfiguration.objects.get_or_create()

    # Виводить повідомлення в консоль, щоб бачити прогрес міграції
    print('\n[Configuration] Створено екземпляр конфігурації за замовчуванням.')

    # Створює базові типи завдань, щоб система не була порожньою
    TaskType.objects.get_or_create(name='Simple', defaults={'cost': 100.00})
    TaskType.objects.get_or_create(name='Medium', defaults={'cost': 250.00})
    TaskType.objects.get_or_create(name='Complex', defaults={'cost': 500.00})

    print('[Configuration] Створено базові типи завдань.')


class Migration(migrations.Migration):
    # Ця міграція виконується після початкової міграції '0001_initial',
    # яка створює самі таблиці в базі даних.
    dependencies = [
        ('configuration', '0001_initial'),
    ]

    # Вказує Django, що під час застосування цієї міграції
    # потрібно виконати функцію `create_default_configuration`.
    operations = [
        migrations.RunPython(create_default_configuration),
    ]