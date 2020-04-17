# Generated by Django 3.0.5 on 2020-04-15 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0002_auto_20200415_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorsExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name="code de l'erreur")),
                ('counter', models.IntegerField(default=0, verbose_name="compteur de l'erreur")),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name="Auteur de l'exercice")),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.Exercise')),
                ('submission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exercises.Submission', verbose_name='Submission link')),
            ],
        ),
    ]