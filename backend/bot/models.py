from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseTag, AbstractBaseStatement
from django.db import models
from ckeditor.fields import RichTextField

STATEMENT_TEXT_MAX_LENGTH = 65535


class Question(models.Model):
    """Question model used in the app."""

    title = models.TextField(
        verbose_name="question type (pas de ponctuation,majuscule)"
    )
    matched = models.BooleanField(
        verbose_name="possède une réponse associée", default=False
    )
    asked = models.IntegerField(
        verbose_name="nombre de fois que la question a été posée", default=1
    )

    class Meta(object):
        """The Meta class to define more fields."""

        ordering = ["title"]
        verbose_name = "Question"

    def __str__(self):
        """Return string representation of the object."""
        return "{0} [{1}] - {2}".format(
            self.matched, self.asked, self.title
        )


class Answer(models.Model):
    """Answer model used in the app."""

    answer = RichTextField()
    question = models.ManyToManyField(Question)

    def __str__(self):
        """Return string representation of the object."""
        return self.answer

    class Meta(object):
        verbose_name = "Réponse"


class Tag(AbstractBaseTag):
    pass


class Statement(AbstractBaseStatement):
    text = models.CharField(
        max_length=STATEMENT_TEXT_MAX_LENGTH
    )

    search_text = models.CharField(
        max_length=STATEMENT_TEXT_MAX_LENGTH,
        blank=True
    )

    in_response_to = models.CharField(
        max_length=STATEMENT_TEXT_MAX_LENGTH,
        null=True
    )

    search_in_response_to = models.CharField(
        max_length=STATEMENT_TEXT_MAX_LENGTH,
        blank=True
    )

    tags = models.ManyToManyField(
        "bot.Tag",
        related_name='bot_statements'
    )
