from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError
from movies.models import Movie, Genre, UserRating
from django.core.exceptions import ValidationError


class GenreModelTests(TestCase):
    def setUp(self):
        self.drama = Genre.objects.create(genre='Action')

    def test_genre_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(genre='Action')


class MovieModelTests(TestCase):

    def setUp(self):
        self.drama = Genre.objects.create(genre='Drama')
        self.movie = Movie.objects.create(title="Mare of Easttown", year=2021, imdb_rating=9.0)
        self.movie.genre.add(self.drama)

    def test_object_fields_are_correct(self):
        self.assertEqual(self.movie.title, "Mare of Easttown")
        self.assertEqual(self.movie.year, 2021)
        self.assertEqual(self.movie.imdb_rating, 9.0)
        self.assertEqual(str(self.movie.genre.all()[0]), 'Drama')
        self.assertEqual(str(self.movie), "Mare of Easttown (2021)")

    def test_a_movie_can_have_more_than_one_genre(self):
        crime = Genre.objects.create(genre='Crime')
        self.movie.genre.add(crime)
        self.assertEqual(str(self.movie.genre.all()[0]), 'Drama')
        self.assertEqual(str(self.movie.genre.all()[1]), 'Crime')
        self.assertEqual(self.movie.genre.all().count(), 2)

    def test_movie_year_is_cinema_is_invented_raises_validatin_error(self):
        with self.assertRaises(ValidationError):
            self.movie.year = 1700
            self.movie.full_clean()

    def test_movie_year_3000_raises_validatin_error(self):
        with self.assertRaises(ValidationError):
            self.movie.year = 3000
            self.movie.full_clean()


class UserRatingTests(TestCase):
    def setUp(self):
        data = {'email': 'testuser@test.com',
                'date_of_birth': "1990-01-01",
                'country': 'TR',
                'gender': 'X',
                'password': 'superpass123?*'}
        User = get_user_model()
        self.user = User.objects.create_user(**data)
        self.drama = Genre.objects.create(genre='Action')
        self.drama = Genre.objects.create(genre='Drama')
        self.movie = Movie.objects.create(title="Mare of Easttown", year=2021, imdb_rating=9.0)
        self.movie.genre.add(self.drama)
        self.user_rating = 5
        self.genre = UserRating.objects.create(movie=self.movie, user=self.user, user_rating=self.user_rating)

    def test_object_fields_are_correct(self):
        self.assertEqual(self.genre.movie, self.movie)
        self.assertEqual(self.genre.user, self.user)
        self.assertEqual(self.genre.user_rating, 5)
        self.assertEqual(str(self.genre),
                         f'{self.movie.title} ({self.movie.year}) takes {self.user_rating}/5 by {self.user}')
