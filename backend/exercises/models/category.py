from django.db import models


class Category(models.Model):
    """Category object model."""

    name = models.CharField(
        max_length=127, unique=True, verbose_name="Catégorie de l'exercice"
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Catégorie n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "catégorie"
