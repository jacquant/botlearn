from django.db import models


class ErrorCount(models.Model):
    """ErrorCount model class."""

    error = models.ForeignKey(
        to="exercises.Error",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Erreur link",
    )
    counter = models.IntegerField(
        verbose_name="compteur de l'erreur", default=0
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "{0} - {1}X".format(self.error, self.counter)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "erreur comptage"
