from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created

from memoire.settings import DEFAULT_FROM_EMAIL


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """
    context = {
        "last_name": reset_password_token.user.last_name,
        "first_name": reset_password_token.user.first_name,
        "reset_password_url": "{}reset_password?token={}".format(
            settings.FRONT_URL, reset_password_token.key
        ),
    }

    html_message = render_to_string("mails/user/reset_password.html", context)
    plain_message = strip_tags(html_message)

    mail_subject = "Changement de mot de passe SITE AGE"

    send_mail(
        subject=mail_subject,
        message=plain_message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[reset_password_token.user.mail],
        html_message=html_message,
    )
