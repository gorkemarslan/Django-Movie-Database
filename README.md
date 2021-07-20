[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://raw.githubusercontent.com/gorkemarslan/Django-Movie-Database/main/LICENSE)
# Django-Movie-Database

Make migrations first:

```
$ python manage.py makemigrations
$ python manage.py migrate
```

Execute the command below to load initiai Movie and Genre data:
```
$ python manage.py load_initial_data
```
*(It might take a while.)*


Then, run the server:
```
$ python manage.py runserver
```
