# Generated by Django 3.0.4 on 2020-03-09 15:00

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import (
    migrations,
    models,
)

import constrainedfilefield.fields.file

import exercises.models.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sandbox", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=127,
                        unique=True,
                        verbose_name="Catégorie de l'exercice",
                    ),
                ),
            ],
            options={"verbose_name": "catégorie",},
        ),
        migrations.CreateModel(
            name="Difficulty",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        verbose_name="Numéro d'identification"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=127,
                        unique=True,
                        verbose_name="Nom de la difficulté",
                    ),
                ),
            ],
            options={"verbose_name": "difficulté",},
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="nom de l'exercice"
                    ),
                ),
                (
                    "due_date",
                    models.DateTimeField(
                        verbose_name="Date à laquelle rendre"
                    ),
                ),
                (
                    "instruction",
                    models.TextField(verbose_name="Consignes de l'exercice"),
                ),
                (
                    "project_files",
                    constrainedfilefield.fields.file.ConstrainedFileField(
                        content_types=["application/gzip"],
                        default="",
                        mime_lookup_length=4096,
                        storage=exercises.models.utils.OverwriteStorage(),
                        upload_to=exercises.models.utils.path_and_rename,
                        validators=[
                            exercises.models.utils.validate_file_extensions
                        ],
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur de l'exercice",
                    ),
                ),
                (
                    "difficulty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="exercises.Difficulty",
                        verbose_name="Difficulté de l'exercice",
                    ),
                ),
                (
                    "dockerImage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sandbox.SandboxProfile",
                        verbose_name="Image docker associée",
                    ),
                ),
            ],
            options={"verbose_name": "exercice",},
        ),
        migrations.CreateModel(
            name="Requirement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        verbose_name="Nom de la dépendance",
                    ),
                ),
            ],
            options={"verbose_name": "requirement",},
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Nom du tag"
                    ),
                ),
            ],
            options={"verbose_name": "tag",},
        ),
        migrations.CreateModel(
            name="TargetStudents",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
            ],
            options={
                "verbose_name": "étudiant cible",
                "verbose_name_plural": "étudiants cibles",
            },
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "submission_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Moment de la soumission",
                    ),
                ),
                ("code_input", models.TextField()),
                (
                    "code_output",
                    django.contrib.postgres.fields.jsonb.JSONField(),
                ),
                (
                    "final",
                    models.BooleanField(
                        default=False, verbose_name="Type de la soumission"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur de la soumission",
                    ),
                ),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exercises.Exercise",
                        verbose_name="Exercice lié à la soumission",
                    ),
                ),
            ],
            options={"verbose_name": "soumission",},
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        verbose_name="Nom de la séance",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Date de la séance"
                    ),
                ),
                ("visibility", models.BooleanField(default=False)),
                ("activated", models.BooleanField(default=True)),
                (
                    "in_charge_persons",
                    models.ManyToManyField(
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Les personnes responsables",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="exercises.TargetStudents",
                        verbose_name="Séance à destination de ce type d'étudiants",
                    ),
                ),
            ],
            options={"verbose_name": "TP",},
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "academic_year",
                    models.CharField(
                        max_length=20, verbose_name="Année académique"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("number", models.PositiveSmallIntegerField()),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="exercises.Section",
                    ),
                ),
            ],
            options={
                "verbose_name": "section",
                "unique_together": {("parent", "number")},
            },
        ),
        migrations.AddField(
            model_name="exercise",
            name="requirements",
            field=models.ManyToManyField(
                blank=True,
                related_name="exercises_requirements",
                to="exercises.Requirement",
                verbose_name="Dépendances associées",
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="exercises.Section",
                verbose_name="Section de l'exercice",
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="exercises.Session",
                verbose_name="Session de l'exercice",
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="exercises_tags",
                to="exercises.Tag",
                verbose_name="Tags associés",
            ),
        ),
    ]
