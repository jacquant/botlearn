from django.db import models

from ckeditor.fields import RichTextField


class Question(models.Model):
    """Question model used in the app."""

    title = models.TextField(
        verbose_name="question type (pas de ponctuation,majuscule)"
    )
    matched = models.BooleanField(
        verbose_name="possède une réponse associée", default=True
    )
    asked = models.IntegerField(
        verbose_name="nombre de fois que la question a été posée", default=1
    )

    class Meta(object):
        """The Meta class to define more fields."""

        ordering = ["intitule"]

    def __str__(self):
        """Return string representation of the object."""
        return "{0} [{1}] - {2}".format(
            self.matched, self.asked, self.intitule
        )


class Answer(models.Model):
    """Answer model used in the app."""

    answer = RichTextField()
    question = models.ManyToManyField(Question)

    def __str__(self):
        """Return string representation of the object."""
        return self.reponse
