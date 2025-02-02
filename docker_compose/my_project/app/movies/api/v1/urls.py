from django.urls import path
from movies.views import MoviesListApi, MoviesDetailApi  # Импорт представлений

urlpatterns = [
    path('movies/', MoviesListApi.as_view(), name='movies-list'),
    path('movies/<uuid:pk>/', MoviesDetailApi.as_view(), name='movies-detail'),
]
