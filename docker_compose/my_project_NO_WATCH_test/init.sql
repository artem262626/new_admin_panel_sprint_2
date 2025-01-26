- Создание пользователя "app" с паролем 'qwerty1234'
CREATE USER app WITH PASSWORD 'qwerty1234';

-- Создание базы данных movies_database
CREATE DATABASE movies_database;

-- Подключение к новой базе данных
\c movies_database

-- Создание схемы для таблиц
CREATE SCHEMA IF NOT EXISTS content;

-- Установление схемы по умолчанию
SET search_path TO content, public;

-- Предоставляем привилегии пользователю "app" для работы со схемой
GRANT ALL PRIVILEGES ON SCHEMA content TO app;

-- Изменение владельца базы данных на пользователя "app"
ALTER DATABASE movies_database OWNER TO app;
