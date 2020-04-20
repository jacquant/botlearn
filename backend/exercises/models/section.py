from django.db import models


class Section(models.Model):
    """Section model class."""

    academic_year = models.CharField(
        max_length=20, verbose_name="Année académique"
    )
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.PROTECT
    )
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "Section n°{number} ({academic_year}) - {name}".format(
            number=self.number,
            academic_year=self.academic_year,
            name=self.name,
        )

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "section"
        unique_together = (
            "parent",
            "number",
        )
