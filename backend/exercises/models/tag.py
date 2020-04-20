from django.db import models


class Tag(models.Model):
    """Tag model class."""

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Nom du tag"
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Tag n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "tag"
