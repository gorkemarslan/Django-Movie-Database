[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://raw.githubusercontent.com/gorkemarslan/Django-Movie-Database/main/LICENSE)


# Django-Movie-Database

## About

> You rate, we recommend!

This is the motto of the project.  Movies that are matched with ratings given by a user to the varied movies on the platform are recommended to the user.

Of course, to get the recommended movies, the user has to have an account.
Needless to say, only authenticated users are able to give ratings to the movies.
Apart from these features, all users (authenticated and anonymous) can take a look at movies and their detail information such as director, poster etc.

There are totally 9742 movies with 18 genres on the platform. The data is available inside [data](https://github.com/gorkemarslan/Django-Movie-Database/tree/main/data) directory.

Two separate data files are responsible for launching the project.

 - `movie_data.csv` includes movie titles and genres
 - `ratings.csv` includes dataset of users and their ratings (1-5) for movies.

## Getting Started

You need to have [Docker](https://www.docker.com/) on your machine to work with this project.

Then, you are able to build docker files with these commands:

    $ docker build 
    $ docker-compose up -d --build

If everything's fine, then you're ready to make migrations:

```
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
$ docker-compose up -d
```

Execute the command below to load initial Movie and Genre data:
*(It might take a while since the amount of 10k movies will be loaded.)*
```
$ docker-compose exec web python manage.py load_initial_data
$ docker-compose up -d
```

That is it! Now you can start exploring the project.
