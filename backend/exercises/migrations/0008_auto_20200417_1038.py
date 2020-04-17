# Generated by Django 3.0.5 on 2020-04-17 08:38

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0007_submission_not_executed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='errorexercise',
            name='code',
        ),
        migrations.RemoveField(
            model_name='errorexercise',
            name='counter',
        ),
        migrations.CreateModel(
            name='ErrorCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(default=0, verbose_name="compteur de l'erreur")),
                ('error', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exercises.Error', verbose_name='Erreur link')),
            ],
            options={
                'verbose_name': 'erreur comptage',
            },
        ),
        migrations.AddField(
            model_name='errorexercise',
            name='errors',
            field=models.ManyToManyField(blank=True, related_name='exercises_errors', to='exercises.ErrorCount', verbose_name='Erreurs détectées'),
        ),
    ]