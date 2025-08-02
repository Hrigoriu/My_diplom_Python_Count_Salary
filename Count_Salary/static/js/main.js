/**
 * Він керує логікою всіх віджетів на бічній панелі: погодою, годинником та календарем.
 */
document.addEventListener('DOMContentLoaded', function () {

    // --- НАЛАШТУВАННЯ: СПИСОК ДОСТУПНИХ МІСТ ---
    // Тут список міст, які будуть доступні у випадаючому меню.
    const CITIES = {
        'Україна': [
            'Київ', 'Вінниця', 'Дніпро', 'Донецьк', 'Житомир', 'Запоріжжя',
            'Івано-Франківськ', 'Кропивницький', 'Луганськ', 'Луцьк', 'Львів',
            'Миколаїв', 'Одеса', 'Полтава', 'Рівне', 'Суми', 'Тернопіль',
            'Ужгород', 'Харків', 'Херсон', 'Хмельницький', 'Черкаси',
            'Чернівці', 'Чернігів'
        ]
    };

    // --- Посилання на HTML-елементи, з якими будемо працювати ---
    const citySelect = document.getElementById('city-select');
    const weatherContent = document.getElementById('weather-content');
    const clockDisplay = document.getElementById('clock-display');
    const dateDisplay = document.getElementById('date-display');
    const calendarDisplay = document.getElementById('calendar-display');

    /**
     * ВІДЖЕТ ПОГОДИ
     */
    // Заповнює випадаючий список містами з константи CITIES
    function populateCitySelect() {
        for (const country in CITIES) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = country;
            CITIES[country].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                optgroup.appendChild(option);
            });
            citySelect.appendChild(optgroup);
        }
    }

    // Асинхронна функція для отримання даних про погоду з нашого Django-сервера
    async function fetchWeather(city) {
        weatherContent.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>'; // Індикатор завантаження
        try {
            const response = await fetch(`/widgets/api/weather/?city=${encodeURIComponent(city)}`);
            const data = await response.json();

            if (response.ok) { // Якщо HTTP-статус 200-299
                weatherContent.innerHTML = `
                    <img id="weather-icon" src="https://openweathermap.org/img/wn/${data.icon}@2x.png" alt="${data.description}">
                    <h3 class="mb-0">${Math.round(data.temperature)}°C</h3>
                    <p class="text-muted">${data.description}</p>
                `;
            } else { // Якщо сервер повернув помилку (напр. 400, 404)
                weatherContent.innerHTML = `<p class="text-danger small">${data.error}</p>`;
            }
        } catch (error) { // Якщо сталася помилка мережі
            weatherContent.innerHTML = '<p class="text-danger small">Не вдалося завантажити погоду.</p>';
        }
    }

    /**
     * ВІДЖЕТ ГОДИННИКА ТА ДАТИ
     */
    function updateClock() {
        const now = new Date();
        clockDisplay.textContent = now.toLocaleTimeString('uk-UA'); // Формат HH:MM:SS

        // Ручне форматування дати для правильного відмінка дня тижня ("середа")
        let weekday = now.toLocaleDateString('uk-UA', { weekday: 'long' });
        weekday = weekday.charAt(0).toUpperCase() + weekday.slice(1);
        const datePart = now.toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric' });
        dateDisplay.textContent = `${weekday}, ${datePart}`;
    }

    /**
     * ВІДЖЕТ КАЛЕНДАРЯ
     */
    function renderCalendar() {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth();
        const today = now.getDate();

        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDayAdjusted = (firstDayOfMonth === 0) ? 6 : firstDayOfMonth - 1; // 0=Пн, 6=Нд

        let html = '<table class="table table-bordered table-sm text-center"><thead><tr>';
        ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'].forEach(d => html += `<th>${d}</th>`);
        html += '</tr></thead><tbody><tr>';

        for (let i = 0; i < firstDayAdjusted; i++) html += '<td></td>';

        for (let day = 1; day <= daysInMonth; day++) {
            if ((day + firstDayAdjusted - 1) % 7 === 0 && day > 1) html += '</tr><tr>';
            html += `<td class="${day === today ? 'bg-primary text-white rounded' : ''}">${day}</td>`;
        }

        let lastDayIndex = (firstDayAdjusted + daysInMonth - 1) % 7;
        while(lastDayIndex < 6) {
            html += '<td></td>';
            lastDayIndex++;
        }

        html += '</tr></tbody></table>';
        calendarDisplay.innerHTML = html;
    }

    /**
     * ІНІЦІАЛІЗАЦІЯ - код, який запускається один раз при завантаженні сторінки
     */
    populateCitySelect(); // Заповнюємо список міст

    // Зчитуємо останнє вибране місто з пам'яті браузера
    const savedCity = localStorage.getItem('selectedCity') || 'Київ';
    citySelect.value = savedCity;
    fetchWeather(savedCity); // Завантажуємо погоду для цього міста

    // Додаємо слухача подій: при зміні міста, зберігаємо вибір і оновлюємо погоду
    citySelect.addEventListener('change', (event) => {
        const newCity = event.target.value;
        localStorage.setItem('selectedCity', newCity);
        fetchWeather(newCity);
    });

    // Запускаємо годинник та календар
    updateClock();
    renderCalendar();
    setInterval(updateClock, 1000); // Налаштовуємо оновлення годинника кожну секунду
});