from django.conf import settings
from django.template import loader
from django.urls import reverse
from django.utils.translation import ugettext as _

from django_comments_xtd.utils import send_mail


def notify_emailaddr_change_confirmation(
    key, user, email, site,
    text_template="users/notifications/emailaddr_change_confirmation.txt",
    html_template="users/notifications/emailaddr_change_confirmation.html"
):
    """Send email requesting email-address change confirmation."""
    subject = _("Request to change your account's email address")
    confirmation_url = reverse("change-email-confirm",
                               args=[key.decode('utf-8')])
    message_context = {'user': user,
                       'new_email': email,
                       'confirmation_url': confirmation_url,
                       'contact': settings.COMMENTS_XTD_FROM_EMAIL,
                       'site': site}
    # Prepare text message.
    text_message_template = loader.get_template(text_template)
    text_message = text_message_template.render(message_context)
    if settings.COMMENTS_XTD_SEND_HTML_EMAIL:
        # prepare html message
        html_message_template = loader.get_template(html_template)
        html_message = html_message_template.render(message_context)
    else:
        html_message = None

    send_mail(subject, text_message, settings.COMMENTS_XTD_FROM_EMAIL,
              [email,], html=html_message)
