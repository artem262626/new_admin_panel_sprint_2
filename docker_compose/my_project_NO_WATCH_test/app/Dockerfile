FROM python:3.10

# Устанавливаем зависимости
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Сбор статических файлов 
RUN python manage.py collectstatic --noinput 

# Команда для запуска uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]
