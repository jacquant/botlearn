from django.db import models


class TargetStudents(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "Étudiant cible n°{id} - {name}".format(id=self.id, name=self.name)

    class Meta:
        verbose_name = "étudiant cible"
        verbose_name_plural = "étudiants cibles"
