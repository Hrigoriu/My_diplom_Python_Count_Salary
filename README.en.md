# Salary Accounting System (My_diplom_Python_Count_Salary)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

[Українська версія (Ukrainian version)](README.ukr.md)

---

A web application built with Django for managing employee records and automatically calculating their monthly salaries. The project is designed with a strong focus on OOP principles to ensure clean code, flexibility, and scalability.

### ✨ Key Features

-   **Employee Management**: Full CRUD (Create, Read, Update, Delete) for employee data.
-   **Salary Period Tracking**: Create monthly salary records for each employee, specifying hours worked, currency exchange rates, and the value of completed tasks.
-   **Automatic Salary Calculation**: The system automatically calculates the salary upon each record save, using a flexible formula.
-   **Flexible Configuration System**: Global parameters (base rates, coefficients) are easily editable through the Django admin panel.
-   **Multi-currency Display**: Salary is displayed in UAH, USD, and EUR.
-   **Search and Sorting**: An interactive employee table with the ability to search by name and sort by name or seniority level.
-   **Pagination**: The employee list is automatically paginated for convenience.
-   **Interactive Widgets**: A sidebar with a real-time clock, a calendar, and a weather widget that updates in real time.
-   **Automatic Demo Data Seeding**: A custom migration creates 20 employees and fills their salary history for 2 years for immediate demonstration.

### 🛠️ Technology Stack

-   **Backend**: Python 3, Django
-   **Database**: SQLite
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS), Bootstrap 5 (CDN)
-   **Key Python Libraries**:
    -   `django-crispy-forms` & `crispy-bootstrap5` for form rendering.
    -   `django-solo` for implementing the Singleton pattern in settings.
    -   `requests` for making HTTP requests to the weather API.

### 🚀 Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [URL of your repository]
    cd My_diplom_Python_Count_Salary
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **⚠️ IMPORTANT: Configure the Weather API Key!**
    *   Open the file `My_diplom_Python_Count_Salary/settings.py`.
    *   Find the line `OPENWEATHER_API_KEY = "your-api-key-goes-here"`.
    *   Replace `"your-api-key-goes-here"` with your actual API key from [OpenWeatherMap](https://openweathermap.org/). **The weather widget will not work without this.**

5.  **Apply database migrations:**
    *   This command will create the `db.sqlite3` database, automatically populate the initial settings, and seed the demo data (employees and their salaries).
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.