# Generated by Django 3.0.7 on 2020-06-14 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20200612_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Réponse'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['title'], 'verbose_name': 'Question'},
        ),
    ]