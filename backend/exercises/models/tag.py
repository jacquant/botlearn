from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du tag")
