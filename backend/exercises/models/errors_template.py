from django.db import models


class ErrorsTemplate(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nom du template")
    errors = models.ManyToManyField(
        to="exercises.Error",
        related_name="errorsTemplate_errors",
        verbose_name="Erreurs associées",
        blank=True,
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "{0}".format(self.name)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "template d'erreurs"
        verbose_name_plural = "templates d'erreurs"
