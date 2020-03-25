from django.db import models
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Question(models.Model):
    intitule = models.TextField(verbose_name="question type (pas de ponctuation,majuscule)")

    class Meta:
        ordering = ['intitule']

    def __str__(self):
        return self.intitule


class Reponse(models.Model):
    reponse = RichTextField()
    question = models.ManyToManyField(Question)

    def __str__(self):
        return self.reponse
