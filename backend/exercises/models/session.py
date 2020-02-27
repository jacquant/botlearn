from django.db import models


class Session(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nom de la séance"
    )
    date = models.DateTimeField(verbose_name="Date de la séance", blank=True, null=True)
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
        to="accounts.User", verbose_name="Les personnes responsables", blank=True, null=True
    )

    def __str__(self):
        return "TP n°{id} - {name} - du {date}".format(
            id=self.id, name=self.name, date=self.date
        )

    class Meta:
        verbose_name = "TP"
