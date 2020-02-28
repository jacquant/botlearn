from django.db import models
from .utils import path_and_rename


class Exercise(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom de l'exercice")
    due_date = models.DateTimeField(verbose_name="Date à laquelle rendre")
    instruction = models.TextField(verbose_name="Consignes de l'exercice")
    author = models.ForeignKey(
        to="accounts.User",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Auteur de l'exercice",
    )
    difficulty = models.ForeignKey(
        to="exercises.Difficulty",
        on_delete=models.PROTECT,
        verbose_name="Difficulté de l'exercice",
    )
    session = models.ForeignKey(
        to="exercises.Session",
        on_delete=models.CASCADE,
        verbose_name="Session de l'exercice",
    )
    section = models.ForeignKey(
        to="exercises.Section",
        on_delete=models.CASCADE,
        verbose_name="Section de l'exercice",
    )

    tags = models.ManyToManyField(to="exercises.Tag", verbose_name="Tags associés", blank=True, null=True)


    project_files = models.FileField(blank=False, null=True, upload_to=path_and_rename)

    def __str__(self):
        return "Exercice n°{id} - {name} - pour le {due_date}".format(
            id=self.id, name=self.name, due_date=self.due_date
        )

    class Meta:
        verbose_name = "exercice"
