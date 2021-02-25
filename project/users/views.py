from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.views.defaults import bad_request

from django_comments_xtd import signed

from . import forget_me, remember_me
from .forms import EmailForm, LoginForm, PersonalDataForm
from .models import Confirmation
from .utils import notify_emailaddr_change_confirmation


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


@login_required
def edit_user(request,
              email_form_msg="",
              pdata_form_msg="",
              avatar_form_msg=""):
    email_form = EmailForm(user=request.user)
    pdata_form = PersonalDataForm(user=request.user)
    return render(request, 'users/edit_account.html', {
        'email_form': email_form,
        'email_form_msg': email_form_msg,
        'pdata_form': pdata_form,
        'pdata_form_msg': pdata_form_msg,
        # 'avatar_form': avatar_form,
        'avatar_form_msg': avatar_form_msg
    })


@login_required
@require_POST
def post_change_email_form_j(request):
    form = EmailForm(request.POST, user=request.user)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors})

    email = form.cleaned_data['email']
    key = signed.dumps(email, compress=True,
                       extra_key=settings.COMMENTS_XTD_SALT)
    site = get_current_site(request)
    notify_emailaddr_change_confirmation(key, request.user, email, site)
    return JsonResponse({'status': 'success'})


@login_required
def confirm_change_email(request, key):
    try:
        email = signed.loads(key, extra_key=settings.COMMENTS_XTD_SALT)
    except (ValueError, signed.BadSignature) as exc:
        return bad_request(request, exc)

    try:
        confirm = Confirmation.objects.get(email=request.user.email,
                                           purpose="E")
    except Confirmation.DoesNotExist as exc:
        return HttpResponseRedirect(reverse("logout"))

    if confirm.key != email:
        return render(request, 'users/change_email_error.html')

    request.user.email = email
    request.user.save()
    confirm.delete()

    return edit_user(request,
                     email_form_msg=_("Your email address has been changed."))


@login_required
@require_POST
def post_personal_data_form_j(request):
    form = PersonalDataForm(request.POST, user=request.user)
    if not form.is_valid():
        return JsonResponse({'status': 'error',
                             'errors': form.non_field_errors})

    request.user.name = form.cleaned_data['name']
    request.user.url = form.cleaned_data['url']
    request.user.language = form.cleaned_data['language']
    request.user.save()
    return JsonResponse({'status': 'success'})
