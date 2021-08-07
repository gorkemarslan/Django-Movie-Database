from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.messages import get_messages
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

    def test_signup_page_redirects_authenticated_user_to_home_page(self):
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

    def test_sign_up_page_return_new_user(self):
        user_count = get_user_model().objects.count()
        data = {'email': 'testuser@test.com', 'date_of_birth': "1990-01-01", 'country': 'TR', 'gender': 'X',
                'password1': 'superpass123?*', 'password2': 'superpass123?*', 'signup': ['Sign Up']}

        response = self.client.post(reverse('signup'), data)
        self.assertRedirects(response, reverse('login'),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)


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
                'password': 'superpass123?*',
                }
        User = get_user_model()
        self.user = User.objects.create_user(**data)

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

    def test_login_page_redirects_authenticated_user_to_home_page(self):
        self.client.login(email=self.email, password=self.password1)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'),
                             status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_login_view_redirect_on_success(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'),
                                    {'username': self.email,
                                     'password': self.password1,
                                     'login': ['Sign In']})
        self.assertTrue(self.client.login(email=self.email, password=self.password1))
        self.assertRedirects(response, expected_url=reverse('home'), status_code=302, target_status_code=200)

    def test_unregistered_user_cannot_login(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'),
                                    {'username': 'unregistered@mail.com',
                                     'password': self.password1,
                                     'login': ['Sign In']})
        self.assertFalse(self.client.login(email='unregistered@mail.com', password=self.password1))
        self.assertRedirects(response, expected_url=reverse('login'), status_code=302, target_status_code=200)

    def test_user_for_is_inactive_cannot_login(self):
        self.client.logout()
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('login'),
                                    {'username': self.email,
                                     'password': self.password1,
                                     'login': ['Sign In']})
        self.assertRedirects(response, expected_url=reverse('login'), status_code=302, target_status_code=200)
        self.assertFalse(self.client.login(email=self.email, password=self.password1))

    def test_user_with_login_form_is_invalid(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'), {'username': self.email, 'login': ['Sign In']})
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Invalid login details given.', messages)
        self.assertRedirects(response, expected_url=reverse('login'), status_code=302, target_status_code=200)


class AccountPageTests(TestCase):

    def setUp(self):
        self.url = reverse('account')
        self.data = {'email': 'testuser@test.com',
                     'date_of_birth': "1990-01-01",
                     'country': 'TR',
                     'gender': 'X',
                     'password': 'superpass123?*',
                     }
        User = get_user_model()
        self.user = User.objects.create_user(**self.data)

    def test_account_page_only_authenticated_users_access(self):
        self.client.logout()
        self.client.login(email=self.data.get('email'), password=self.data.get('password'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Account')
        self.assertTemplateUsed(response, 'users/account.html')

    def test_account_page_unauthenticated_users_redirecting_to_login_page(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/login/?redirect_to=/account/',
                             status_code=302, target_status_code=200)


class PasswordChangeAndDonePagesTests(TestCase):

    def setUp(self) -> None:
        data = {'email': 'testuser@test.com',
                'date_of_birth': "1990-01-01",
                'country': 'TR',
                'gender': 'X',
                'password': 'superpass123?*'}
        User = get_user_model()
        User.objects.create_user(**data)
        self.client.login(email=data.get('email'), password=data.get('password'))

    def test_html_form_class(self):
        response = self.client.get(reverse('password_change'))
        self.assertContains(response, "form-control")
