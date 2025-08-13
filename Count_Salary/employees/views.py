"""
Views (контролери), які обробляють запити користувачів,
взаємодіють з моделями та рендерять HTML-шаблони.
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q, Case, When, Value, IntegerField
from .models import Employee, SalaryRecord
from .forms import EmployeeForm, SalaryRecordForm


def home(request):
    """View для головної сторінки сайту."""
    return TemplateView.as_view(template_name='index.html')(request)


class EmployeeListView(ListView):
    """
    Відображає список співробітників з пошуком, сортуванням та пагінацією.
    """
    model = Employee
    context_object_name = 'employees'
    template_name = 'employees/employee_list.html'
    paginate_by = 10  # Розбивка списку на сторінки

    def get_queryset(self):
        """
        Перевизначаємо цей метод для додавання кастомної логіки фільтрації та сортування.
        """
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(last_name__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(patronymic__icontains=search_query)
            )
        sort_by = self.request.GET.get('sort')
        if sort_by == 'level':
            # Правильне сортування за ієрархією рівнів
            queryset = queryset.annotate(
                level_order=Case(
                    When(level='JUN', then=Value(1)),
                    When(level='MID', then=Value(2)),
                    When(level='SEN', then=Value(3)),
                    When(level='LEAD', then=Value(4)),
                    default=Value(5), output_field=IntegerField(),
                )
            ).order_by('level_order', 'last_name')
        else:  # Сортування за замовчуванням
            queryset = queryset.order_by('last_name', 'first_name')
        return queryset

    def get_context_data(self, **kwargs):
        """Передаємо параметри запиту в шаблон для коректної роботи пагінації."""
        """Пагінація - розбиття великого списку елементів (наприклад, товарів, статей) на сторінки"""
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        return context


class EmployeeDetailView(DetailView):
    """Відображає детальну інформацію про одного співробітника."""
    model = Employee
    context_object_name = 'employee'
    template_name = 'employees/employee_detail.html'


class EmployeeCreateView(CreateView):
    """Сторінка створення нового співробітника."""
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')


class EmployeeUpdateView(UpdateView):
    """Сторінка редагування існуючого співробітника."""
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')


class SalaryRecordCreateView(CreateView):
    """Сторінка створення нового запису про зарплату."""
    model = SalaryRecord
    form_class = SalaryRecordForm
    template_name = 'employees/salaryrecord_form.html'

    def form_valid(self, form):
        # Прив'язуємо запис до співробітника, ID якого взято з URL
        form.instance.employee = Employee.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Передаємо об'єкт співробітника в шаблон для кнопки "Скасувати" та заголовку
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        # Повертаємо користувача на сторінку деталей цього ж співробітника
        return reverse_lazy('employee-detail', kwargs={'pk': self.kwargs['pk']})


class SalaryRecordUpdateView(UpdateView):
    """Сторінка редагування запису про зарплату."""
    model = SalaryRecord
    form_class = SalaryRecordForm
    template_name = 'employees/salaryrecord_form.html'

    def get_success_url(self):
        employee = self.object.employee
        return reverse_lazy('employee-detail', kwargs={'pk': employee.pk})


class SalaryRecordDeleteView(DeleteView):
    """Сторінка підтвердження видалення запису про зарплату."""
    model = SalaryRecord
    template_name = 'employees/salaryrecord_confirm_delete.html'

    def get_success_url(self):
        employee = self.object.employee
        return reverse_lazy('employee-detail', kwargs={'pk': employee.pk})