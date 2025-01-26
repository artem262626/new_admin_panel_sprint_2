import pytest
import psycopg2
import sqlite3
import os
import datetime
from os import environ
from dotenv import load_dotenv
from datetime import datetime
import logging

# Настройки для подключения к PostgreSQL
load_dotenv()
POSTGRES_CONNECT = {
    'dbname': environ.get('DB_NAME'),
    'user': environ.get('DB_USER'),
    'password': environ.get('DB_PASSWORD'),
    'host': environ.get('DB_HOST'),
    'port': environ.get('DB_PORT'),
    'options': '-c search_path=content'
}

# Настройки для подключения к SQLite
SQLITE_CONFIG = 'db.sqlite'

# Настройка логирования
logging.basicConfig(
    filename='db_comparison.log',  # имя файла для сохранения логов
    level=logging.INFO,             # уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@pytest.fixture
def postgres_connection():
    """Создает соединение с базой данных PostgreSQL."""
    connection = psycopg2.connect(**POSTGRES_CONNECT)
    yield connection
    connection.close()

@pytest.fixture
def sqlite_connection():
    """Создает соединение с базой данных SQLite."""
    connection = sqlite3.connect(SQLITE_CONFIG)
    yield connection
    connection.close()

def get_record_count(connection, table_name):
    """Получает количество записей в заданной таблице."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def get_records(connection, table_name):
    """Получает все записи в заданной таблице."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    records = cursor.fetchall()
    cursor.close()
    return records

def compare_records(postgres_records, sqlite_records, table_name):
    """Сравнивает записи между PostgreSQL и SQLite и выводит, какие поля не совпадают."""
    for postgres_record, sqlite_record in zip(postgres_records, sqlite_records):
        record_differences = {}
        for index, (pg_field, sqlite_field) in enumerate(zip(postgres_record, sqlite_record)):
            if pg_field != sqlite_field:
                record_differences[f'Field {index}'] = {'Postgres': pg_field, 'SQLite': sqlite_field}
        
        if record_differences:
            logging.warning(
                f"Записи в таблице {table_name} не совпадают! Различия: {record_differences}"
            )
            return False
    return True

def test_record_counts(postgres_connection, sqlite_connection):
    """Сравнивает количество записей в таблицах между PostgreSQL и SQLite."""
    table_names = ['genre', 'film_work', 'person', 'genre_film_work', 'person_film_work']
    for table_name in table_names:
        postgres_count = get_record_count(postgres_connection, table_name)
        sqlite_count = get_record_count(sqlite_connection, table_name)
        logging.info(f"{table_name}: Postgres count={postgres_count}, SQLite count={sqlite_count}")
        
        assert postgres_count == sqlite_count, (
            f"Количество записей в PostgreSQL для таблицы {table_name}: {postgres_count}, "
            f"в SQLite: {sqlite_count}. Не равны!"
        )
        
        # Сравнение содержимого таблиц
        postgres_records = get_records(postgres_connection, table_name)
        sqlite_records = get_records(sqlite_connection, table_name)

        if not compare_records(postgres_records, sqlite_records, table_name):
            assert False, (
                f"Содержимое таблицы {table_name} не совпадает! "
                f"Сравнение завершено. Смотрите логи для подробной информации."
            )
        else:
            logging.info(f"Содержимое таблицы {table_name} совпадает.")
