from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    class GenderType(models.TextChoices):
        NONE = "", "----"
        FEMALE = "F", _("Female")
        MALE = "M", _("Male")
        X_GENDER = "X", _("X")

    email = models.EmailField(_('email_address'), max_length=100, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GenderType.choices, default=GenderType.NONE, max_length=4)
    country = CountryField()
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'gender', 'country']

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email
