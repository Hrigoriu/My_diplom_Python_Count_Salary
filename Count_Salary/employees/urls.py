"""
URL-маршрути для додатку 'employees'.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Список співробітників (головна сторінка додатку)
    path('', views.EmployeeListView.as_view(), name='employee-list'),

    # Створення нового співробітника
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),

    # Сторінка деталей, редагування співробітника
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),

    # Створення запису про зарплату для конкретного співробітника (pk - це ID співробітника)
    path('<int:pk>/salary/create/', views.SalaryRecordCreateView.as_view(), name='salary-create'),

    # Редагування та видалення конкретного запису про зарплату (pk - це ID запису про зарплату)
    path('salary/<int:pk>/update/', views.SalaryRecordUpdateView.as_view(), name='salary-update'),
    path('salary/<int:pk>/delete/', views.SalaryRecordDeleteView.as_view(), name='salary-delete'),
]