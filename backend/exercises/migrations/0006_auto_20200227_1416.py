# Generated by Django 3.0.3 on 2020-02-27 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20200225_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date de la séance'),
        ),
    ]