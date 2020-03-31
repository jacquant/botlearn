from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=127, unique=True, verbose_name="Catégorie de l'exercice")

    def __str__(self):
        return "Catégorie n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta:
        verbose_name = "catégorie"
