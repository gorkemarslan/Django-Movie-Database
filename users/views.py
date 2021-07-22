from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect


class AccountPageView(generic.TemplateView):
    template_name = 'users/account.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(AccountPageView, self).dispatch(request, *args, **kwargs)


def signup_login_handler(request):
    """
    Using FBV to handle two different form in a same page is pretty convenient than using CBV
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        if request.method == 'POST':
            signup_form = CustomUserCreationForm()
            login_form = CustomAuthenticationForm()
            if request.POST.get('login'):
                login_form = CustomAuthenticationForm(request, data=request.POST)
                if login_form.is_valid():
                    email = login_form.cleaned_data.get('username')
                    password = login_form.cleaned_data.get('password')
                    user = authenticate(username=email, password=password)
                    if user:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {email}.")
                        return HttpResponseRedirect(reverse_lazy('home'))
                    # else:
                    #     messages.error(request, "Invalid login details given.")
                    #     return HttpResponseRedirect(reverse_lazy('login'))
                else:
                    messages.error(request, "Invalid login details given.")
                    return HttpResponseRedirect(reverse_lazy('login'))

            elif request.POST.get('signup'):
                signup_form = CustomUserCreationForm(request.POST)
                if signup_form.is_valid():
                    user = signup_form.save()
                    messages.success(request, f'Account created for {user.email}.\n Now, you can login!')
                    return HttpResponseRedirect(reverse_lazy('login'))

        else:
            signup_form = CustomUserCreationForm()
            login_form = CustomAuthenticationForm()

        return render(request, 'users/signup_login.html', {
            'signup_form': signup_form,
            'login_form': login_form,
        })
