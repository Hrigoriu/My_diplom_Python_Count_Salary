import os
import sys


def main():
    """Виконання адміністративних завдань."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Count_Salary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Не можеш завантажити Django. Ви впевнені, що він встановлений ?'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
