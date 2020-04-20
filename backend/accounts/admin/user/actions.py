from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from django_rest_passwordreset.models import (
    ResetPasswordToken,
    clear_expired,
    get_password_reset_lookup_field,
    get_password_reset_token_expiry_time,
)
from django_rest_passwordreset.views import (
    HTTP_IP_ADDRESS_HEADER,
    HTTP_USER_AGENT_HEADER,
    ResetPasswordRequestToken,
)
from rest_framework import exceptions

from accounts.models.user import User
from accounts.signals.user import password_reset_token_created


def send_reset_password(modeladmin, request, queryset):
    """Action function to send a mail with reset information."""
    for element_user in queryset:
        # before we continue, delete all existing expired tokens
        clear_expired_tokens()

        # find a user by email address (case insensitive search)
        users = check_active_user_by_mail(element_user.mail)

        # last but not least: iterate over all users that are active and can
        # change their password
        # and create a Reset Password Token and send a signal with the created
        # token
        for user in users:
            if user.eligible_for_reset():
                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(
                            HTTP_USER_AGENT_HEADER, ""
                        ),
                        ip_address=request.META.get(
                            HTTP_IP_ADDRESS_HEADER, ""
                        ),
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for
                # the password reset
                password_reset_token_created(
                    sender=ResetPasswordRequestToken.__class__,
                    instance=ResetPasswordRequestToken,
                    reset_password_token=token,
                )


send_reset_password.short_description = (
    "Propose la réinitialisation des mots de passes à ces utilisateurs!"
)


def clear_expired_tokens():
    """Function used to clear existing and expired tokens."""
    password_reset_token_validation_time = (
        get_password_reset_token_expiry_time()
    )

    # datetime.now minus expiry hours
    now_minus_expiry_time = timezone.now() - timedelta(
        hours=password_reset_token_validation_time
    )

    # delete all tokens where created_at < now - 24 hours
    clear_expired(now_minus_expiry_time)


def check_active_user(active_user_found, field_leakage):
    """Function to check if it exists active user."""
    django_reset_leakage = getattr(settings, field_leakage, default=False)
    return not active_user_found and not django_reset_leakage


def check_active_user_by_mail(email):
    """Check that the requested email is linked to active account.

    :param email: the email requested to reset the token.
    :type email: str
    :raises exceptions.ValidationError: [description]
    :return: a queryset of active users
    :rtype: Queryset<User>
    """
    users = User.objects.filter(
        **{
            "{passwoord}__iexact".format(
                passwoord=get_password_reset_lookup_field()
            ): email
        },
    )

    active_user_found = False

    # iterate over all users and check if there is any user that is active
    # also check whether the password can be changed (is useable), as there
    # could be users that are not allowed
    # to change their password (e.g., LDAP user)
    for user in users:
        if user.eligible_for_reset():
            active_user_found = True

    # No active user found, raise a validation error
    # but not if DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE == True
    if check_active_user(  # noqa: WPS337
        active_user_found, "DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE"
    ):
        raise exceptions.ValidationError(
            {
                "email": [
                    "{0} {1}".format(
                        "There is no active user associated with this e-mail",
                        "address or the password can not be changed",
                    )
                ],
            },
        )
    return users
