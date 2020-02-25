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
        verbose_name="Auteur de l'exercice",
    )
    difficulty = models.ForeignKey(
        to="exercises.Difficulty",
        on_delete=models.PROTECT,
        blank=False,
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
    tags = models.ManyToManyField(
        to="exercises.Tag", verbose_name="Tags associés"
    )
    project_files = models.FileField(blank=False, null=True, upload_to=path_and_rename)
