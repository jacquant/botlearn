from django.db import models
from django import forms
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Question(models.Model):
    intitule = models.TextField(verbose_name="question type (pas de ponctuation,majuscule)")
    matched = models.BooleanField(verbose_name="possède une réponse associée", default=True)
    asked = models.IntegerField(verbose_name="nombre de fois que la question a été posée", default=1)

    class Meta:
        ordering = ['intitule']

    def __str__(self):
        return str(self.matched) + " [" + str(self.asked) + "]" + " - " + self.intitule


class Reponse(models.Model):
    reponse = RichTextField()
    question = models.ManyToManyField(Question)

    def __str__(self):
        return self.reponse
