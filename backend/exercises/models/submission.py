from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class Submission(models.Model):
    author = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE, verbose_name="Auteur de la soumission",)
    exercise = models.ForeignKey(
        to="exercises.Exercise", on_delete=models.CASCADE, verbose_name="Exercice lié à la soumission",
    )
    submission_date = models.DateTimeField(verbose_name="Moment de la soumission", default=timezone.now)
    code_input = models.TextField()
    code_output = JSONField()  # TODO définir une sémantique des retours d'exécution
    final = models.BooleanField(default=False, verbose_name="Type de la soumission")

    def __str__(self):
        return "Soumission n°{id} - de {author} - pour l'exercice n° {exercise}".format(
            id=self.id, author=self.author, exercise=self.exercise
        )

    class Meta:
        verbose_name = "soumission"
