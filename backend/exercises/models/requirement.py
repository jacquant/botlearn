from django.db import models


class Requirement(models.Model):
    """Requirement model class."""

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Nom de la dépendance"
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Dépendance n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "requirement"
