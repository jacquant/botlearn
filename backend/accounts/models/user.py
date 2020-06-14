from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model used in the app."""

    mail = models.EmailField(
        max_length=255, unique=True, verbose_name="Adresse e-mail",
    )
    last_name = models.CharField(max_length=40, verbose_name="Nom")
    first_name = models.CharField(max_length=30, verbose_name="Prénom")
    student = models.BooleanField(
        default=True, blank=True, verbose_name="étudiant"
    )
    student_card = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(20000000), MaxValueValidator(21000000)],
        blank=True,
        null=True,
    )
    eid = models.CharField(
        max_length=12, unique=True, verbose_name="Eid étudiant", blank=True
    )

    anonymous = models.BooleanField(default=False)

    USERNAME_FIELD = "mail"
    EMAIL_FIELD = "mail"

    is_staff = models.BooleanField(
        default=False, verbose_name="administrateur"
    )
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["last_name", "first_name"]

    objects = UserManager()  # noqa: WPS110

    class Meta(object):
        """The Meta class of the User Model."""

        verbose_name = "utilisateur"
