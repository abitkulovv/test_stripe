# Django + Stripe Backend

Простой бэкенд на Django с интеграцией Stripe Checkout.

Проект поддерживает: Модель `Item` (name, description, price, currency), Модель `Order` (несколько Item, общая сумма), Stripe Checkout через session для Item и Order, Django Admin для управления Item и Order.

Локальный запуск:
1. Клонируем репозиторий:  
`git clone https://github.com/abitkulovv/test_stripe.git`  
`cd test_stripe`
2. Создаём виртуальное окружение и устанавливаем зависимости:  
`python -m venv venv`  
`source venv/bin/activate` (Linux / Mac)  
`venv\Scripts\activate` (Windows)  
`pip install -r requirements.txt`
3. Создаём файл `.env` рядом с `manage.py`:  
`DJANGO_SECRET_KEY=your-secret-key`  
`DEBUG=True`  
`STRIPE_SECRET_KEY_USD=sk_test_XXXXXXXXXXXXXXXX`  
`STRIPE_PUBLISHABLE_KEY=pk_test_XXXXXXXXXXXXXXXX`
4. Применяем миграции: `python manage.py migrate`
5. Создаём суперпользователя: `python manage.py createsuperuser`
6. Запускаем сервер: `python manage.py runserver`  
Сайт доступен: http://127.0.0.1:8000, админка: http://127.0.0.1:8000/admin

Работа с Stripe: Для тестов используйте карту `4242 4242 4242 4242`. Цена указывается в минимальных единицах (центах для US). Валюта указывается в поле `currency` (`usd`, `eur`, `kgs`). Примеры URL: `/item/1` — страница Item с кнопкой Buy, `/order/1` — страница Order с несколькими Item и Pay Order.

Docker: создаём `.env` с секретами, собираем контейнер `docker-compose build`, запускаем `docker-compose up`. Django автоматически применяет миграции и запускается через Gunicorn. Сайт доступен: http://127.0.0.1:8000

Деплой онлайн (Render / Railway): подключаем репозиторий GitHub, в Environment Variables добавляем `DJANGO_SECRET_KEY`, `DEBUG=False`, `STRIPE_SECRET_KEY_USD`, `STRIPE_PUBLISHABLE_KEY`. После деплоя применяем миграции: `python manage.py migrate` и создаём суперпользователя: `python manage.py createsuperuser`. Открываем `/admin` для проверки и создания Item/Order.

Тестирование: создаём несколько Item через админку, создаём Order и добавляем Item, открываем `/item/1` или `/order/1`, нажимаем Buy / Pay Order → Stripe Checkout, используем тестовую карту `4242 4242 4242 4242`.

Особенности: все Item в одном Order должны быть одной валюты, цена указывается в минимальных единицах (cents), модели доступны в админке.

Ссылки: Репозиторий: https://github.com/abitkulovv/test_stripe
