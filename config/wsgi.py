import os
import django
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Автоматическое создание суперпользователя для Render / деплоя 
django.setup()
User = get_user_model()

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpassword"

try:
    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
        print(f"Superuser '{ADMIN_USERNAME}' создан автоматически")
    else:
        print(f"Superuser '{ADMIN_USERNAME}' уже существует")
except Exception as e:
    print("Ошибка при создании суперпользователя:", e)
