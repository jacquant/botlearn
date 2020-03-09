from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du tag")

    def __str__(self):
        return "Tag n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta:
        verbose_name = "tag"

