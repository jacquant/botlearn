from django.db import models


class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom de la dépendance")

    def __str__(self):
        return "Dépendance n°{id} - {name}".format(
            id=self.id, name=self.name)

    class Meta:
        verbose_name = "requirement"
