
# Установка

1. Установите Python 3.8.5

2. Активируйте виртуальное окружение:

- На Windows:
```bash
venv\Scripts\activate
```
- На macOS/Linux:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install django
pip install psycopg-binary
pip install psycopg2
```

4. В файле settings.py введите данные своей базы Postgres.

# Миграции

Для применения миграций выполните команды:
```bash
python manage.py makemigrations
python manage.py migrate
```

# Запуск сервера

Для запуска локального сервера разработки выполните команду:
```bash
python manage.py runserver
```
После этого сервер будет доступен по адресу http://127.0.0.1:8000/

# Панель админа

1. Создайте админа:
```bash
python manage.py createsuperuser
```

3. Перезапустите локальный сервер.

2. В адресной строке припишите к адресу admin:
http://127.0.0.1:8000/admin

# Запуск тестов

Для запуска тестов выполните команду:
```bash
python manage.py test
```