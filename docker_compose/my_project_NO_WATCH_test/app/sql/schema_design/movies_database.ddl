-- Подключение к базе данных
\c movies_database

-- Создание схемы для таблиц
CREATE SCHEMA IF NOT EXISTS content;

-- Установление схемы по умолчанию
SET search_path TO content,public;

-- Создание таблицы с фильмами
CREATE TABLE IF NOT EXISTS film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

-- Построение индекса для ускорения поиска по дате
CREATE INDEX film_work_creation_date_idx ON film_work(creation_date);

-- Создание таблицы с персонами
CREATE TABLE IF NOT EXISTS person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

-- Создание промежуточной таблицы для фильмов и персон
CREATE TABLE IF NOT EXISTS person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES person (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW()
);

-- Построение индекса для ограничения уникальности фильмов и персон
CREATE UNIQUE INDEX film_work_person_idx ON person_film_work (film_work_id, person_id, role);

-- Создание таблицы с жанрами
CREATE TABLE IF NOT EXISTS genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

-- Создание промежуточной таблицы для фильмов и жанров
CREATE TABLE IF NOT EXISTS genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES film_work (id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES genre (id) ON DELETE CASCADE,
    created timestamp with time zone DEFAULT NOW()
);

-- Построение индекса для ограничения уникальности фильмов и жанров
CREATE UNIQUE INDEX film_work_genre_idx ON genre_film_work (film_work_id, genre_id);
