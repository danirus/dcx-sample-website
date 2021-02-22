from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from .models import Confirmation, User


confirm_pending_msg = _("Your registration process is not finished yet, you  have to confirm your e-Mail address. Check the e-Mail message we already sent you.")
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


email_already_registered = _("This e-Mail address is already registered.")
too_many_attempts = _("Please, wait 24 hours to request another email address change.")


class ChangeEmailForm(forms.Form):
    email = forms.CharField(required=True)

    class Media:
        js = ("js/change_email_form.js",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        if self.user:
            kwargs['initial'] = { 'email': self.user.email }
        super().__init__(*args, **kwargs)

    def clean_email(self):
        # Check if strip is necessary.
        email = self.cleaned_data['email'].strip()

        try:
            if User.objects.filter(email=email).count():
                raise forms.ValidationError(email_already_registered)

            # If there is already an email change confirmation
            # for this user, the update the confirmation.
            confirm = Confirmation.objects.get(email=self.user.email)
            if not confirm.is_out_of_date() and confirm.notifications < 3:
                confirm.key = email
                confirm.notifications += 1
                confirm.save()
                return email

            elif confirm.is_out_of_date():
                confirm.delete()
                Confirmation.objects.create(email=self.user.email, key=email,
                                            purpose="E")  # Change email.
                return email

            else:
                raise forms.ValidationError(too_many_attempts)

        except Confirmation.DoesNotExist as exc:
            Confirmation.objects.create(email=self.user.email, key=email,
                                        purpose="E")  # Change email.
            return email