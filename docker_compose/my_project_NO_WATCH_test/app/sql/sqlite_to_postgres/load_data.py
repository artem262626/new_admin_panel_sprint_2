import logging
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import astuple, fields

import psycopg2
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

current_filename = os.path.basename(__file__).rsplit('.', 1)[0]

logging.basicConfig(
    filename=current_filename + '.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


TABLE_CLASS = {
    'film_work': FilmWork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork
}

BATCH_SIZE = 100

SQLITE_TABLES_FIELDS = {
    'film_work':
        'id,title,description,creation_date,rating,type,created_at,updated_at',
    'genre': 'id,name,description,created_at,updated_at',
    'person': 'id,full_name,created_at,updated_at',
    'genre_film_work': 'id,genre_id,film_work_id,created_at',
    'person_film_work': 'id,film_work_id,person_id,role,created_at'
}

POSTGRES_TABLES_FIELDS = {
    'film_work':
        'id,title,description,creation_date,rating,type,created,modified',
    'genre': 'id,name,description,created,modified',
    'person': 'id,full_name,created,modified',
    'genre_film_work': 'id,genre_id,film_work_id,created',
    'person_film_work': 'id,film_work_id,person_id,role,created'
}


class PostgresSaver:
    """Saver in PostgreSQL DB."""
    def __init__(self, pg_conn: _connection, pg_cursor: _cursor):
        self.pg_conn = pg_conn
        self.pg_cursor = pg_cursor
        self.pg_cursor.execute("""
        SET TIMEZONE TO 'UTC';
        """)
        self.pg_conn.commit()

    def save_data_in_table(self, data: list, table_name: str):
        """Execute insert query in PostgreSQL DB.
        Fields for insert are given explicitly from dictionary
        SQLITE_TABLES_FIELDS and vary depending on table_name.
        This method uses ON CONFLICT statement of Postgresql so that
        duplicate insert ignores.

        Args:
            data: list of dataclass objects representing table
            table_name: string name of table for insert

        Returns:
            None

        """
        if table_name not in TABLE_CLASS:
            raise sqlite3.Error('There is no such table in database')

        number_of_params = len(fields(data[0]))
        placeholders = ','.join('%s' for _ in range(number_of_params))
        fields_for_insert = POSTGRES_TABLES_FIELDS[table_name]
        args = ','.join(
            self.pg_cursor.mogrify(
                f'({placeholders})', astuple(item)
            ).decode() for item in data
        )
        match table_name:
            case 'film_work_person':
                restriction = """
                ON CONFLICT (film_work_id, person_id, role) DO NOTHING;
                """

            case _:
                restriction = 'ON CONFLICT (id) DO NOTHING;'
        query = f"""
        INSERT INTO {table_name}({fields_for_insert})
        VALUES{args}
        {restriction}
        """
        self.pg_cursor.execute(query)


class SQLiteExtractor:
    """Extractor of data from SQLite DB with batch of specified size."""
    def __init__(self, connection: sqlite3.Connection):
        self.cursor = None
        self.connection = connection
        self.batch_size = None

    def get_data_from_table(self, table_name: str,
                            batch_size: int = 100):
        """Executes select query from SQLite DB.


        Args:
            table_name: string name of table for insert
            batch_size: int size of batch for extract and yield

        Yields:
            list of dataclass objects

        """
        query = "SELECT {0} FROM {1};".format(
            SQLITE_TABLES_FIELDS[table_name],
            table_name
        )
        self.cursor = self.connection.execute(query)
        self.batch_size = batch_size
        data_class = TABLE_CLASS[table_name]
        rows = self.cursor.fetchmany(batch_size)
        while rows := self.cursor.fetchmany(batch_size):
            yield [
                data_class(**row) for row in rows
        ]


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection, pg_cursor: _cursor):
    """Main method for uploading data from SQLite to Postgres"""

    postgres_saver = PostgresSaver(pg_conn, pg_cursor)
    sqlite_extractor = SQLiteExtractor(connection)

    for table_name in TABLE_CLASS:
        try:
            for data in sqlite_extractor.get_data_from_table(
                    table_name,
                    BATCH_SIZE
            ):
                try:
                    postgres_saver.save_data_in_table(data, table_name)
                except psycopg2.Error as ps_e:
                    logging.error(
                        f'Error during writing to {table_name} \n->\t{ps_e}'
                    )
                    break
        except sqlite3.Error as sq_e:
            logging.error(
                f'Error during reading from SQLite to {table_name}\n->\t{sq_e}')
            break
        except Exception as e:
            logging.error(f"Error occured!\n\t->{e}")
        else:
            logging.info(
                "Successfully migrated data from SQLITE to POSTGRESQL"
            )


if __name__ == '__main__':
    logging.info('Start reading from sqlite and write to postgres')

    load_dotenv()

    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
        'options': '-c search_path=content'
    }

    with conn_context('db.sqlite') as sqlite_conn, \
            psycopg2.connect(
                **dsl,
                cursor_factory=DictCursor
            ) as pg_conn, pg_conn.cursor() as pg_cursor:
        load_from_sqlite(sqlite_conn, pg_conn, pg_cursor)
