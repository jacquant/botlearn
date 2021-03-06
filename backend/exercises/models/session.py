from django.db import models


class Session(models.Model):
    """Session model class."""

    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nom de la séance"
    )
    date = models.DateTimeField(
        verbose_name="Date de la séance", blank=True, null=True
    )
    visibility = models.BooleanField(default=False)
    activated = models.BooleanField(default=True)
    target = models.ForeignKey(
        to="exercises.TargetStudents",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Séance à destination de ce type d'étudiants",
    )
    in_charge_persons = models.ManyToManyField(
        to="accounts.User",
        verbose_name="Les personnes responsables",
        blank=True,
    )

    def __str__(self):
        """Return a string getter.

        :return: String formattage of the object
        :rtype: str
        """
        return "{name} - du {date}".format(name=self.name, date=self.date)

    class Meta(object):
        """The Meta class that defines some fields."""

        verbose_name = "TP"
