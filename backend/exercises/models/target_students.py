from django.db import models


class TargetStudents(models.Model):
    """TargetStudent model class."""

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Étudiant cible n°{id} - {name}".format(
            id=self.id, name=self.name
        )

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "étudiant cible"
        verbose_name_plural = "étudiants cibles"
