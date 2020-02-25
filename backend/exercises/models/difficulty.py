from django.db import models


class Difficulty(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name="Numéro d'identification")
    name = models.CharField(max_length=127, unique=True, verbose_name="Nom de la difficulté")

    def __str__(self):
        return "Difficulté n°{number} - {name}".format(number=self.number, name=self.name)

    class Meta:
        verbose_name = "difficulté"