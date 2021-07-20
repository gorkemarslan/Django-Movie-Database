from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from users.views import signup_login_handler


class SignupPageTests(TestCase):

    email = 'testuser@test.com'
    date_of_birth = "1990-01-01"
    country = 'TR'
    gender = 'M'
    password1 = 'superpass123?**?'
    password2 = 'superpass123?**?'

    def setUp(self):
        self.url = reverse('signup')

    def test_signup_template(self):
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'users/signup_login.html')
        self.assertTemplateNotUsed(self.response, 'users/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Wrong Content!')

    def test_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(
            view.func.__name__,
            signup_login_handler.__name__
        )

    def test_signup_page_redirects_logged_user_to_home_page(self):
        data = {'email': 'testuser@test.com',
                'date_of_birth': "1990-01-01",
                'country': 'TR',
                'gender': 'X',
                'password': 'superpass123?*'}
        User = get_user_model()
        User.objects.create_user(**data)
        self.client.login(email=data.get('email'), password=data.get('password'))
        response = self.client.get(reverse('signup'))
        self.assertRedirects(response, reverse('home'),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)


class LoginPageTests(TestCase):

    email = 'testuser@test.com'
    date_of_birth = "1990-01-01"
    country = 'TR'
    gender = 'X'
    password1 = 'superpass123?*'
    password2 = 'superpass123?*'

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)
        data = {'email': 'testuser@test.com',
                'date_of_birth': "1990-01-01",
                'country': 'TR',
                'gender': 'X',
                'password': 'superpass123?*'}
        User = get_user_model()
        User.objects.create_user(**data)

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'users/signup_login.html')
        self.assertTemplateNotUsed(self.response, 'users/login.html')
        self.assertContains(self.response, 'Sign In')
        self.assertNotContains(self.response, 'Wrong Content!')

    def test_login_view(self):
        view = resolve('/login/')
        self.assertEqual(
            view.func.__name__,
            signup_login_handler.__name__
        )

    def test_login_page_redirects_logged_user_to_home_page(self):

        self.client.login(email=self.email, password=self.password1)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_login_view_redirect_on_success(self):

        self.client.logout()

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.client.login(username=self.email, password=self.password1))
        response = self.client.post(reverse('login'))
        self.assertRedirects(response, expected_url=reverse('home'), status_code=302, target_status_code=200)
