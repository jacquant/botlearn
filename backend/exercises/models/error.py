from django.db import models


TYPES = (
    ("error", "Error"),
    ("warning", "Warning"),
    ("advice", "Advice"),
)


class Error(models.Model):
    """Error model class."""

    code = models.CharField(
        unique=True, max_length=10, verbose_name="code de l'erreur"
    )
    message = models.CharField(
        max_length=1000, verbose_name="message de l'erreur", default=""
    )
    type_error = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        choices=TYPES,
        verbose_name="type d'erreur",
        default="error",
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Code - {0}".format(self.code)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "erreur"
