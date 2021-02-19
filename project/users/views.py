from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

from . import forget_me, remember_me
from .forms import LoginForm


def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            if request.GET.get("next"):
                response = HttpResponseRedirect(request.GET.get("next"))
            else:
                response = HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            if form.cleaned_data.get("remember"):
                remember_me(response, form.user)
            login(request, form.user)
            return response
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    response = HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.LANGUAGE_CODE)
    forget_me(response)
    logout(request)
    return response


@login_required
def user_account(request):
    return render(request, 'users/account.html')