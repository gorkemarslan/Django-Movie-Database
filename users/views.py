from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm, CustomPasswordChangeForm


class AccountPageView(LoginRequiredMixin, generic.UpdateView):
    # LoginRequiredMixin
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    # UpdateView
    template_name = 'users/account.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('account')

    def get_object(self, **kwargs):
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change.html'


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change_done.html'


def signup_login_handler(request):
    """
    Using FBV to handle two different form in a same page is pretty convenient than using CBV
    """
    # Only anonymous users are able to access the login and signup pages.
    # If a user is authenticated, then redirects the user to the home page.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        if request.method == 'POST':
            signup_form = CustomUserCreationForm()
            login_form = CustomAuthenticationForm()
            # If login form is submitted.
            if request.POST.get('login'):
                login_form = CustomAuthenticationForm(request, data=request.POST)
                if login_form.is_valid():
                    email = login_form.cleaned_data.get('username')
                    password = login_form.cleaned_data.get('password')
                    user = authenticate(username=email, password=password)
                    # If user credentials are correct, then login
                    if user:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {email}.")
                        return HttpResponseRedirect(reverse_lazy('home'))
                    # If not, display message error in the template and redirect login page.
                    else:
                        messages.error(request, "Invalid login details given.")
                        return HttpResponseRedirect(reverse_lazy('login'))
                else:
                    messages.error(request, "Invalid login details given.")
                    return HttpResponseRedirect(reverse_lazy('login'))

            # If signup form is submitted.
            elif request.POST.get('signup'):
                signup_form = CustomUserCreationForm(request.POST)
                if signup_form.is_valid():
                    user = signup_form.save()
                    messages.success(request, f'Account created for {user.email}.\n Now, you can login!')
                    return HttpResponseRedirect(reverse_lazy('login'))
                else:
                    return render(request, 'users/signup_login.html', {
                        'signup_form': signup_form,
                        'login_form': login_form,
                        'error_in_signup': True
                    })

        else:
            signup_form = CustomUserCreationForm()
            login_form = CustomAuthenticationForm()

        return render(request, 'users/signup_login.html', {
            'signup_form': signup_form,
            'login_form': login_form,
        })
