import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import InvalidPage
from django.http import Http404
from django.utils.translation import gettext as _
from .recommendation import recommender
from .models import Movie, UserRating


class HomePageView(TemplateView):
    template_name = 'movies/home.html'


class MovieListView(ListView):
    model = Movie
    paginate_by = 10
    context_object_name = 'movie_list'
    template_name = 'movies/movie_list.html'

    def post(self, *args, **kwargs):
        return post_star_rating(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context['user_rating'] = UserRating.objects.all()
        return context

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        # Now page queries can be float. If it is, make it float() first, then apply int()
        # Remember that page is an instance of str class
        try:
            page_number = int(float(page))
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))

        try:
            if page_number > paginator.num_pages:
                page_number = paginator.num_pages
            elif page_number <= 0:
                page_number = 1
            page = paginator.page(page_number)
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })


class MovieDetailView(DetailView):
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


class MovieRecommendationView(TemplateView):

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


class UserStarsListView(ListView):
    paginate_by = 50
    context_object_name = 'user_stars_list'
    template_name = 'movies/user_stars_list.html'

    def post(self, *args, **kwargs):
        return post_star_rating(self, *args, **kwargs)

    def get_queryset(self):
        """
        Returns movie by following traversal relationship through:
        user -> user_rating -> movie
        """
        return Movie.objects.filter(user_rating__user=self.request.user)


def post_star_rating(obj, *args, **kwargs):
    """
    A function to handle star ratings in ListViews
    Example usage in a ListView:
    .. code-block:: python
        def post(self, *args, **kwargs):
            return post_star_rating(self, *args, **kwargs)
    """
    # Check AJAX requests
    is_ajax = obj.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
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
        return JsonResponse({"success": True}, status=200)

    return JsonResponse({"success": False}, status=400)
