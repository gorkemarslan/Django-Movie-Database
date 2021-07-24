[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://raw.githubusercontent.com/gorkemarslan/Django-Movie-Database/main/LICENSE)
# Django-Movie-Database

Make migrations first:

```
$ python manage.py makemigrations
$ python manage.py migrate
```

Execute the command below to load initiai Movie and Genre data:
*(It might take a while.)*
```
$ python manage.py load_initial_data
```
There are 9742 movies, 18 genres. The command above loads entire data to the project.

Then, run the server:
```
$ python manage.py runserver
```
