from django.core.management.base import BaseCommand
import os
from django.conf import settings
from movies.models import Movie, Genre
import csv
from django.core.management import call_command


def genre_to_obj(genre_name):
    return Genre.objects.get(genre=genre_name)


def load_genre_data_from_json():
    call_command('loaddata', 'genre_data.json', app_label='movies')


def load_movie_data_from_csv():
    DATA_FILE = 'data/movie_data.csv'

    path = os.path.join(settings.BASE_DIR, DATA_FILE)
    line = 0
    with open(path) as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            # print(line)
            line += 1
            if line == 1:
                continue
            new_movie, created = Movie.objects.get_or_create(
                title=row[1],
                year=row[3],
            )
            genre_list = row[2].split('|')
            genre_queryset = map(genre_to_obj, genre_list)
            list_queryset = list(genre_queryset)
            new_movie.genre.add(*list_queryset)
            new_movie.save()


class Command(BaseCommand):
    def handle(self, **options):
        if not Genre.objects.exists():
            load_genre_data_from_json()
            print('Genres have been loaded.')
        if not Movie.objects.exists():
            load_movie_data_from_csv()
            print('Movies have been loaded.')
