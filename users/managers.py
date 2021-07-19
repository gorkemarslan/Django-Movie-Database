from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom User Model Manager where email is the unique identifier for authentication.
    """

    def create_user(self, email, password, date_of_birth, gender, country, **extra_fields):
        """
        Create and save a user with the given email address, date of birth, country and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, gender=gender, country=country, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, date_of_birth, gender, country, **extra_fields):
        """
        Create and save a superuser with the given email address and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, date_of_birth=date_of_birth,
                                gender=gender, country=country, **extra_fields)
