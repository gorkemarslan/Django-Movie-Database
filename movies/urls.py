from django.urls import path
from .views import MovieListView, MovieRecommendationView, MovieDetailView


urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<uuid:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('recommendation/', MovieRecommendationView.as_view(), name='recommendation'),
]
