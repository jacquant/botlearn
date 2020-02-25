from django.db import models


class Session(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nom de la séance"
    )
    date = models.DateTimeField(verbose_name="Date de la séance")
    visibility = models.BooleanField(default=False)
    activated = models.BooleanField(default=True)
    target = models.ForeignKey(
        to="exercises.TargetStudents",
        blank=False,
        on_delete=models.PROTECT,
        verbose_name="Séance à destination de ce type d'étudiants",
    )
    in_charge_persons = models.ManyToManyField(to="accounts.User", verbose_name="Les personnes responsables")

