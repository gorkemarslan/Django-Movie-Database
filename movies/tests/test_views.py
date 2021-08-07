from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from movies.models import UserRating, Movie, Genre


class MovieListViewTests(TestCase):
    def setUp(self):
        self.url = reverse('movie_list')
        genre = Genre.objects.create(genre='Animation')
        self.movie = Movie.objects.create(title='Toy Story', year=1995, imdb_rating=8.3)
        self.movie.genre.add(genre)
        self.user_data = {'email': 'testuser@test.com',
                          'date_of_birth': "1990-01-01",
                          'country': 'TR',
                          'gender': 'X',
                          'password': 'superpass123?*'}
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.data = {'movie_id': self.movie.pk, 'rating': 5, 'delete_rating': False}

    def test_a_user_can_rates_a_unrated_movie(self):
        self.client.login(email=self.user_data.get('email'), password=self.user_data.get('password'))
        self.response = self.client.post(self.url, self.data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(UserRating.objects.count(), 1)
        self.assertEqual(UserRating.objects.first().user_rating, 5)

    def test_a_user_can_change_rating_of_a_movie(self):
        UserRating.objects.create(user=self.user, movie=self.movie, user_rating=4)
        self.client.login(email=self.user_data.get('email'), password=self.user_data.get('password'))
        response = self.client.post(self.url, self.data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json.get('success'))
        self.assertEqual(UserRating.objects.count(), 1)
        self.assertEqual(UserRating.objects.first().user_rating, 5)

    def test_a_user_can_delete_rating_of_a_movie(self):
        UserRating.objects.create(user=self.user, movie=self.movie, user_rating=4)
        rating_data = {'movie_id': self.movie.pk, 'rating': 4, 'delete_rating': True}
        self.client.login(email=self.user_data.get('email'), password=self.user_data.get('password'))
        response = self.client.post(self.url, rating_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json.get('success'))
        self.assertFalse(UserRating.objects.exists())

    def test_invalid_post_request(self):
        self.client.login(email=self.user_data.get('email'), password=self.user_data.get('password'))
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'success': False})
        self.assertFalse(UserRating.objects.exists())


class MovieDetailViewTests(TestCase):
    def setUp(self):
        genre = Genre.objects.create(genre='Animation')
        self.movie = Movie.objects.create(title='Toy Story', year=1995, imdb_rating=8.3)
        self.movie.genre.add(genre)

    def test_movie_detail_with_correct_url(self):
        response = self.client.get(self.movie.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_with_incorrect_url(self):
        response = self.client.get('/movies/123456/')
        self.assertEqual(response.status_code, 404)

    def test_movie_detail_view(self):
        response = self.client.get(self.movie.get_absolute_url())
        self.assertContains(response, 'Toy Story')
        self.assertTemplateUsed(response, 'movies/movie_detail.html')


class MovieRecommendationViewTests(TestCase):

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)
        data = {'email': 'testuser@test.com',
                'date_of_birth': "1990-01-01",
                'country': 'TR',
                'gender': 'X',
                'password': 'superpass123?*'}
        User = get_user_model()
        user = User.objects.create_user(**data)

        genre = Genre.objects.create(genre='Animation')
        movie = Movie.objects.create(title='Toy Story', year=1995, imdb_rating=8.3)
        movie.genre.add(genre)
        UserRating.objects.create(movie=movie, user=user, user_rating=4)
        self.client.login(email=data.get('email'), password=data.get('password'))

        self.url = reverse('recommendation')
        self.response = self.client.get(self.url)

    def test_data(self):
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(UserRating.objects.count(), 1)

    def test_context(self):
        self.assertIsNotNone(self.response.context.get('recommendation_list'))


class PaginationTests(TestCase):

    def setUp(self):
        self.url = reverse('movie_list')
        self.query = '?page='
        self.url = self.url + self.query

    def test_page_is_valid_int_number(self):
        page = self.url + '2'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 200)

    def test_page_is_float_number(self):
        page = self.url + '1.5'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 200)

    def test_page_is_last(self):
        page = self.url + 'last'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 200)

    def test_page_is_a_string_but_not_last_raises_404(self):
        page = self.url + 'lastttt'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 404)

    def test_page_is_a_very_large_number(self):
        page = self.url + '1234556789'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 200)

    def test_page_is_a_negative_number(self):
        page = self.url + '-1'
        self.response = self.client.get(page)
        self.assertEqual(self.response.status_code, 200)


class SearchingMovieTests(TestCase):
    def setUp(self):
        self.search_url = reverse('search')
        self.query = '?q=' + "toy"
        self.url = self.search_url + self.query
        genre = Genre.objects.create(genre='Animation')
        movie = Movie.objects.create(title='Toy Story', year=1995, imdb_rating=8.3)
        movie.genre.add(genre)

    def test_search_result_is_correct_for_correct_words(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Toy Story")

    def test_search_result_is_correct_for_wrong_words(self):
        url = self.search_url + '?q=' + "abc"
        response = self.client.get(url)
        self.assertNotContains(response, "Toy Story")
