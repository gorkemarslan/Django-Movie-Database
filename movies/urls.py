from django.urls import path
from .views import HomePageView, MovieListView, MovieRecommendationView, MovieDetailView
from .views import UserStarsListView, SearchResultsListView, AboutPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<uuid:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('recommendation/', MovieRecommendationView.as_view(), name='recommendation'),
    path('stars/', UserStarsListView.as_view(), name='user_stars_list'),
    path('search/', SearchResultsListView.as_view(), name='search'),
    path('about/', AboutPageView.as_view(), name='about'),
]
