from django.db import models


class Error(models.Model):
    """Error model class."""

    code = models.CharField(
        unique=True, max_length=10, verbose_name="code de l'erreur"
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
