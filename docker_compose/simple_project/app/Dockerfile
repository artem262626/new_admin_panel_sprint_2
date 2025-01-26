FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UWSGI_PROCESSES=1
ENV UWSGI_THREADS=16
ENV UWSGI_HARAKIRI=240
ENV DJANGO_SETTINGS_MODULE='example.settings'


COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY uwsgi/uwsgi.ini uwsgi.ini
COPY run_uwsgi.sh run_uwsgi.sh
COPY . .

RUN mkdir -p /var/www/static/ \
    && mkdir -p /var/www/media/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN chmod +x run_uwsgi.sh
ENTRYPOINT ["./run_uwsgi.sh"]
