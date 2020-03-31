from django.db import models
from .utils import path_and_rename, validate_file_extensions, OverwriteStorage
from constrainedfilefield.fields import ConstrainedFileField


class Exercise(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom de l'exercice")
    due_date = models.DateTimeField(verbose_name="Date à laquelle rendre")
    instruction = models.TextField(verbose_name="Consignes de l'exercice")
    author = models.ForeignKey(
        to="accounts.User", on_delete=models.PROTECT, blank=True, null=True, verbose_name="Auteur de l'exercice",
    )
    difficulty = models.ForeignKey(
        to="exercises.Difficulty", on_delete=models.PROTECT, verbose_name="Difficulté de l'exercice",
    )
    session = models.ForeignKey(to="exercises.Session", on_delete=models.CASCADE, verbose_name="Session de l'exercice",)
    section = models.ForeignKey(to="exercises.Section", on_delete=models.CASCADE, verbose_name="Section de l'exercice",)

    tags = models.ManyToManyField(
        to="exercises.Tag", related_name="exercises_tags", verbose_name="Tags associés", blank=True,
    )

    project_files = ConstrainedFileField(
        upload_to=path_and_rename,
        validators=[validate_file_extensions],
        content_types=["application/gzip"],
        default="",
        storage=OverwriteStorage(),
    )

    requirements = models.ManyToManyField(
        to="exercises.Requirement",
        related_name="exercises_requirements",
        verbose_name="Dépendances associées",
        blank=True,
    )

    dockerImage = models.ForeignKey(
        to="sandbox.SandboxProfile",
        on_delete=models.CASCADE,
        verbose_name="Image docker associée",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Exercice n°{id} - {name} - pour le {due_date}".format(
            id=self.id, name=self.name, due_date=self.due_date
        )

    class Meta:
        verbose_name = "exercice"
