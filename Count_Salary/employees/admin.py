"""
Налаштування відображення моделей додатку 'employees' в адмін-панелі Django.
"""

from django.contrib import admin
from .models import Employee, SalaryRecord

class SalaryRecordInline(admin.TabularInline):
    """
    Дозволяє відображати та редагувати записи про зарплату
    безпосередньо на сторінці редагування співробітника.
    """
    model = SalaryRecord
    extra = 1 # Показувати одне порожнє поле для додавання нового запису

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Налаштування для моделі Employee в адмін-панелі."""
    list_display = ('get_full_name', 'level') # Колонки, що відображаються у списку
    list_filter = ('level',) # Фільтр збоку
    search_fields = ('last_name', 'first_name') # Поля, за якими працює пошук
    inlines = [SalaryRecordInline] # Підключення SalaryRecordInline

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    """Налаштування для моделі SalaryRecord в адмін-панелі."""
    list_display = ('__str__', 'calculated_salary', 'month', 'year')
    list_filter = ('year', 'month', 'employee__level')
    search_fields = ('employee__last_name', 'employee__first_name')
