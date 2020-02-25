from django.db import models


class Section(models.Model):
    academic_year = models.CharField(max_length=20, verbose_name="Année académique")
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            "parent",
            "number",
        )
