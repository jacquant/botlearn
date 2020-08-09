from django.db import models
from django.utils import timezone


class Submission(models.Model):
    """Submission model class."""

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
    submission_date = models.DateTimeField(
        verbose_name="Moment de la soumission", default=timezone.now,
    )
    code_input = models.TextField()
    not_executed = models.BooleanField(default=False)
    code_output = models.JSONField()
    final = models.BooleanField(
        default=False, verbose_name="Type de la soumission est finale"
    )
    errors = models.ManyToManyField(
        to="exercises.ErrorCount",
        related_name="exercises_errors",
        verbose_name="Erreurs détectées",
        blank=True,
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Soumission n°{id} - {author} - exercice n° {exercise}".format(
            id=self.id, author=self.author, exercise=self.exercise,
        )

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "soumission"
