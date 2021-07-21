from django.contrib import admin
from .models import Genre, Movie, UserRating


class GenreAdmin(admin.ModelAdmin):
    ordering = ['genre']


class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ('movie_id',)
    filter_horizontal = ['genre']
    search_fields = ('title',)


class UserRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)
admin.site.register(UserRating, UserRatingAdmin)
admin.site.register(Genre, GenreAdmin)
