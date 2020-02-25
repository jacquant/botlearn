from django.db import models
from django.contrib.postgres.fields import JSONField


class Submission(models.Model):
    author = models.ForeignKey(
        to="accounts.User",
        on_delete=models.CASCADE,
        verbose_name="Auteur de la soumission",
    )
    exercise = models.ForeignKey(
        to="exercises.Exercise",
        on_delete=models.CASCADE,
        verbose_name="Exercice lié à la soumission",
    )
    code_input = models.TextField()
    code_output = JSONField()  # TODO définir une sémantique des retours d'exécution
    final = models.BooleanField(default=False, verbose_name="Type de la soumission")
