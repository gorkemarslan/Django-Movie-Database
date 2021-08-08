import requests
from django.conf import settings
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .recommendation import recommender
from .models import Movie, UserRating
from .paginations import custom_paginate_queryset


class HomePageView(generic.TemplateView):
    template_name = 'movies/home.html'


class AboutPageView(generic.TemplateView):
    template_name = 'movies/about.html'


class MovieListView(generic.ListView):
    model = Movie
    context_object_name = 'movie_list'
    template_name = 'movies/movie_list.html'
    paginate_by = 10

    def post(self, *args, **kwargs):
        """
        HTTP post method to give star ratings to a movie in the movie list.
        """
        return post_star_rating(self, *args, **kwargs)

    def paginate_queryset(self, queryset, page_size):
        return custom_paginate_queryset(self, queryset, page_size)


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        movie_id = self.object.movie_id
        movie = Movie.objects.get(movie_id=movie_id)
        omdb_request_raw = f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&'
        omdb_request = f'{omdb_request_raw}t={movie.title.replace(" ", "+")}&y={movie.year}'
        response = requests.get(omdb_request)
        json_response = response.json()
        context['plot'] = json_response.get('Plot', 'N/A')
        context['imdb_rating'] = json_response.get('imdbRating', 'N/A')
        context['director'] = json_response.get('Director', 'N/A')
        context['stars'] = json_response.get('Actors', 'N/A')
        context['country'] = json_response.get('Country', 'N/A')
        context['run_time'] = json_response.get('Runtime', 'N/A')
        context['poster_url'] = json_response.get('Poster')
        return context


class MovieRecommendationView(generic.TemplateView):

    template_name = "movies/movie_recommendation.html"

    def post(self, *args, **kwargs):
        post_star_rating(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovieRecommendationView, self).get_context_data(**kwargs)
        # Recommendations are provided only to logged-in users.
        if self.request.user.is_authenticated:
            if UserRating.objects.filter(user=self.request.user):
                recommended_titles = recommender(self.request.user)
                context['recommendation_list'] = [Movie.objects.filter(title=t).first() for t in recommended_titles]
            else:
                context['recommendation_list'] = Movie.objects.all()[:10]
        return context


class UserStarsListView(generic.ListView):
    context_object_name = 'user_stars_list'
    template_name = 'movies/user_stars_list.html'
    paginate_by = 50

    def post(self, *args, **kwargs):
        return post_star_rating(self, *args, **kwargs)

    def get_queryset(self):
        """
        Returns movie by following traversal relationship through:
        user -> user_rating -> movie
        """
        return Movie.objects.filter(user_rating__user=self.request.user)

    def paginate_queryset(self, queryset, page_size):
        return custom_paginate_queryset(self, queryset, page_size)


class SearchResultsListView(generic.ListView):
    context_object_name = 'search_movie_list'
    template_name = 'movies/search_results.html'
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Movie.objects.filter(Q(title__icontains=query))

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def paginate_queryset(self, queryset, page_size):
        return custom_paginate_queryset(self, queryset, page_size)


def post_star_rating(obj, *args, **kwargs):
    """
    The function to handle star ratings in ListViews
    Example usage in a ListView:
    .. code-block:: python
        def post(self, *args, **kwargs):
            return post_star_rating(self, *args, **kwargs)
    """
    # Check AJAX requests
    is_ajax = obj.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        # Get data from the POST request
        user_request = obj.request.user
        movie_id_request = obj.request.POST['movie_id']
        rating_request = int(obj.request.POST['rating'])
        delete_request = eval(obj.request.POST['delete_rating'])
        user = get_user_model().objects.get(email=user_request)
        movie = Movie.objects.get(movie_id=movie_id_request)
        if not delete_request:
            try:
                user_rating_obj = UserRating.objects.get(user=user, movie=movie)
                user_rating_obj.user_rating = rating_request
                user_rating_obj.save()
            except ObjectDoesNotExist:
                UserRating.objects.create(user=user, movie=movie, user_rating=rating_request)
            except Exception:
                pass
        else:
            try:
                user_rating_obj = UserRating.objects.get(user=user, movie=movie, user_rating=rating_request)
                user_rating_obj.delete()
            except Exception:
                pass
        return JsonResponse({"success": True,
                             "rating_average": movie.get_average_rating(),
                             "rating_count": movie.user_rating.count()},
                            status=200)

    return JsonResponse({"success": False}, status=400)
