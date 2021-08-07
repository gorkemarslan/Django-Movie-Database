from django.urls import path
from .views import AccountPageView, signup_login_handler
from .views import CustomPasswordChangeView, CustomPasswordChangeDoneView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', signup_login_handler, name='login'),
    path('signup/', signup_login_handler, name='signup'),
    path('account/', AccountPageView.as_view(), name='account'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
