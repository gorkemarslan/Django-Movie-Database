from django.urls import path
from .views import HomePageView, signup_login_handler
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', signup_login_handler, name='login'),
    path('signup/', signup_login_handler, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),
]
