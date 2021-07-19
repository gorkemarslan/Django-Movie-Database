from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect


class HomePageView(generic.TemplateView):
    template_name = 'users/home.html'


def signup_login_handler(request):
    signup_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    if request.method == 'POST':
        if request.POST.get('login'):
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=email, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {email}.")
                        return HttpResponseRedirect(reverse_lazy('home'))
                    else:
                        messages.error(request, "Your account was inactive.")
                else:
                    messages.error(request, "Invalid login details given.")
            else:
                messages.error(request, "Invalid login details given.")

        elif request.POST.get('signup'):
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('email')
                messages.success(request, f'Account created for {username}!')
                return redirect('home')
    else:
        signup_form = CustomUserCreationForm()
        login_form = CustomAuthenticationForm()
    return render(request, 'users/signup_login.html', {
        'signup_form': signup_form,
        'login_form': login_form,
    })
