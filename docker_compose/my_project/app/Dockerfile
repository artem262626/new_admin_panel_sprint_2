FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV DJANGO_SETTINGS_MODULE=config.settings 

WORKDIR /code 

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean 

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput 

RUN mkdir -p /app/uwsgi  


COPY uwsgi/uwsgi.ini /app/uwsgi/uwsgi.ini  

COPY ./entrypoint.sh /code/entrypoint.sh 
RUN chmod +x /code/entrypoint.sh 

ENTRYPOINT ["/code/entrypoint.sh"]
