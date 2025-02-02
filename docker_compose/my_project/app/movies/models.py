from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255) # перевод _('') name
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = 'content\"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        movie = ('movie', _('Фильм'))
        tv_show = ('tv_show', _('Шоу')) 
        soap_opera  = ('soap_opera', _('Сериал')) 
        cartoon = ('cartoon', _('Мультфильм')) 
    type = models.CharField(_('type'),
        max_length=10,
        choices=Type.choices,
        default=Type.movie
    ) 
    title = models.CharField(_('title'), max_length=255) 
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('Дата создания'),  blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True, default=0,
             validators=[MinValueValidator(0),
             MaxValueValidator(100)])

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    class Meta:
        db_table = 'content\"."film_work'
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        indexes = [
            models.Index(fields=["creation_date"])
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'content\"."genre_film_work'
        indexes = [
            models.Index(fields=["film_work_id", "genre_id"])
        ]



class Person(UUIDMixin, TimeStampedMixin):
    full_name =  models.TextField(_('full_name'), blank=True)
    persons  = models.ManyToManyField('Person', through='PersonFilmwork')
    class Meta:
        db_table = 'content\"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')



class PersonFilmwork(UUIDMixin):
    FILM_ROLE_CHOICES = [
        ('director', _('Director')),
        ('actor', _('Actor')),
        ('producer', _('Producer')),
        ('writer', _('Writer')),
        ('actress', _('Actress')),
        ('cinematographer', _('Cinematographer')),
        ('editor', _('Editor')),
        ('production designer', _('Production Designer')),
        ('costumer', _('Costumer')),
        ('sound designer', _('Sound Designer')),
        ('gaffer', _('Gaffer')),
    ]
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255, choices=FILM_ROLE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\"."person_film_work'
        indexes = [
            models.Index(fields=["film_work_id", "person_id", "role"])
        ]
