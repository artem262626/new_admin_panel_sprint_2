from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def _aggregate_person(self, role):
        return ArrayAgg("persons__full_name", filter=Q(personfilmwork__role=role), distinct=True)


    def get_queryset(self):
        result = self.model.objects.prefetch_related(
            'genres', 
            'persons',
        ).values(
            'id', 
            'title', 
            'description', 
            'creation_date', 
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=self._aggregate_person(role=PersonFilmwork.PersonRole.ACTOR),
            directors=self._aggregate_person(role=PersonFilmwork.PersonRole.DIRECTOR),
            writers=self._aggregate_person(role=PersonFilmwork.PersonRole.WRITER),
        )
        return result

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context) 

class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, 
            self.paginate_by,
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results' : list(page.object_list)
        }

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return kwargs['object']
