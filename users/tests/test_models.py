from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='testuser@mail.com',
                                        password="pass123",
                                        date_of_birth="1990-01-01",
                                        gender='F',
                                        country="FR")

        self.assertEqual(user.email, 'testuser@mail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username field is None for the AbstractUser
            # username field does not exist for the AbstractBaseUser. AttributeError raises.
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='',
                                     password="pass123",
                                     date_of_birth="1990-01-01",
                                     gender='F',
                                     country="FR")

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(email='superuser@mail.com',
                                                  password="superpass123",
                                                  date_of_birth="1990-01-01",
                                                  gender='M',
                                                  country="SW")

        self.assertEqual(superuser.email, 'superuser@mail.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(str(superuser), 'superuser@mail.com')

        try:
            # username field is None for the AbstractUser
            # username field does not exist for the AbstractBaseUser. AttributeError raises.
            self.assertIsNone(superuser.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='superuser@mail.com',
                                          password="superpass123",
                                          date_of_birth="1990-01-01",
                                          gender='M',
                                          country="TR",
                                          is_superuser=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='superuser@mail.com',
                                          password="superpass123",
                                          date_of_birth="1990-01-01",
                                          gender='M',
                                          country="TR",
                                          is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='',
                                          password="superpass123",
                                          date_of_birth="1990-01-01",
                                          gender='M',
                                          country="TR",
                                          is_superuser=True)
