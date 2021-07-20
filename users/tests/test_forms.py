import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from users.forms import CustomUserCreationForm, CustomAuthenticationForm


class SignupFormTests(TestCase):
    email = 'testuser@test.com'
    date_of_birth = datetime.date(1990, 1, 1)
    country = 'TR'
    gender = 'X'
    password1 = 'superpass123?**?'
    password2 = 'superpass123?**?'

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.form = self.response.context.get('signup_form')

    def test_signup_form(self):
        self.assertIsInstance(self.form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_form_valid_data(self):

        data = {'email': self.email, 'date_of_birth': self.date_of_birth,
                'country': self.country, 'gender': self.gender,
                'password1': self.password1, 'password2': self.password2}

        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())


class LoginFormTests(TestCase):

    email = 'testuser@test.com'
    date_of_birth = "1990-01-01"
    country = 'TR'
    gender = 'X'
    password1 = 'superpass123?*'
    password2 = 'superpass123?*'

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)
        self.credentials = {'email': self.email, 'date_of_birth': self.date_of_birth,
                            'country': self.country, 'gender': self.gender,
                            'password': self.password1}
        User = get_user_model()
        self.user = User.objects.create_user(**self.credentials)

    def test_login_form(self):
        form = self.response.context.get('login_form')
        self.assertIsInstance(form, CustomAuthenticationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_login(self):
        self.client.login(email=self.email, password=self.password1)
        response = self.client.post(reverse('login'),
                                    {'username': self.email, 'password': self.password1}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].email, self.email)

    def test_login_form_valid_data(self):
        form_data = {'username': self.email, 'password': self.password1}
        form = CustomAuthenticationForm(None, form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form_data = {}
        form = CustomAuthenticationForm(None, form_data)
        self.assertFalse(form.is_valid())

    def test_login_form_no_password(self):
        form_data = {'username': self.email}
        form = CustomAuthenticationForm(None, form_data)
        self.assertFalse(form.is_valid())

    def test_login_form_no_email(self):
        form_data = {'password': self.password1}
        form = CustomAuthenticationForm(None, form_data)
        self.assertFalse(form.is_valid())
