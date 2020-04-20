from django.db import models


class Difficulty(models.Model):
    """Difficulty model class."""

    number = models.PositiveSmallIntegerField(
        verbose_name="Numéro d'identification"
    )
    name = models.CharField(
        max_length=127, unique=True, verbose_name="Nom de la difficulté"
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Difficulté n°{number} - {name}".format(
            number=self.number, name=self.name,
        )

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "difficulté"
