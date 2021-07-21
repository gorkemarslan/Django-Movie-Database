from django.urls import path
from .views import MovieListView, MovieRecommendationView


urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('recommendation/', MovieRecommendationView.as_view(), name='recommendation'),
]
