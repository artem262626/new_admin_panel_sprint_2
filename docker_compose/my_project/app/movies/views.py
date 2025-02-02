from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from .models import Filmwork, PersonFilmwork, Genre

#class StaffRequiredMixin(UserPassesTestMixin):
#    def test_func(self):
#        return self.request.user.is_staff

#    def handle_no_permission(self):
#        return JsonResponse({'error': 'Forbidden'}, status=403)

class MoviesApiMixin(StaffRequiredMixin, LoginRequiredMixin):
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def get_person_array_agg(role: str):
        return ArrayAgg(
            'personfilmwork__person__full_name',
            filter=Q(personfilmwork__role__icontains=role),
            distinct=True
        )

    def get_queryset(self):
        qs = Filmwork.objects.prefetch_related(
            'genres', 'personfilmwork__person__full_name'
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True
            ),
            actors=MoviesApiMixin.get_person_array_agg('actor'),
            directors=MoviesApiMixin.get_person_array_agg('director'),
            writers=MoviesApiMixin.get_person_array_agg('writer')
        )
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            50
        )

        prev_page = None
        next_page = None
        if page.has_previous():
            prev_page = page.previous_page_number()
        if page.has_next():
            next_page = page.next_page_number()
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(queryset)
        }

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        context = queryset.get(id=self.kwargs['pk'])
        return context
