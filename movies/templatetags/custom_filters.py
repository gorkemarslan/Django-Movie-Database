from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter(name='user_star')
def user_star(user_rating, movie):
    """
    Template tag which allows queryset filtering to get user ratings.
    It gets user.user_rating2 and movie objects.
    Usage:
    .. code-block:: python
    {{ user.user_rating2.all|user_star:movie }}
    """
    try:
        rating = user_rating.get(movie=movie).user_rating
        return rating
    except ObjectDoesNotExist:
        return 0
