from dataclasses import dataclass
from datetime import date, datetime, timezone
from uuid import UUID

from dateutil.parser import parse


@dataclass
class Tables:
    def correct_datetime(self):
        for attr in ('created_at', 'updated_at'):
            if hasattr(self, attr):
                setattr(
                    self,
                    attr,
                    parse(getattr(self, attr)).astimezone(tz=timezone.utc)
                )

    def __post_init__(self):
        self.correct_datetime()


@dataclass
class FilmWork(Tables):
    __slots__ = (
        'id',
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        'created_at',
        'updated_at'
    )
    id: UUID
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre(Tables):
    __slots__ = (
        'id',
        'name',
        'description',
        'created_at',
        'updated_at'
    )
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Person(Tables):
    __slots__ = (
        'id',
        'full_name',
        'created_at',
        'updated_at'
    )
    id: UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWork(Tables):
    __slots__ = (
        'id',
        'genre_id',
        'film_work_id',
        'created_at'
    )
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created_at: datetime


@dataclass
class PersonFilmWork(Tables):
    __slots__ = (
        'id',
        'film_work_id',
        'person_id',
        'role',
        'created_at'
    )
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime
