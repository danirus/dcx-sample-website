from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from .models import Confirmation


confirm_pending_msg = _("Your registration process is not finished yet, you have to confirm your e-Mail address. Check the e-Mail message we already sent you.")
usr_not_active_msg = _("This user account is not active.")
usr_not_auth_msg = _("Enter a correct e-Mail address and password. Note that both fields are case-sensitive.")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(widget=forms.CheckboxInput, required=False,
                                  label=_("Remember me"))

    def __init__(self, *args, **kwargs):
        self.user = None
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(self.request, email=email, password=password)
            if not user:
                raise forms.ValidationError(usr_not_auth_msg)
            else:
                self.user = user
                try:
                    confirmation = Confirmation.objects.get(email=email)
                except Confirmation.DoesNotExist:
                    if not user.is_active:
                        raise forms.ValidationError(usr_not_active_msg)
                else:
                    if not user.is_active:
                        raise forms.ValidationError(confirm_pending_msg)
                    else:
                        confirmation.delete()

        return self.cleaned_data
