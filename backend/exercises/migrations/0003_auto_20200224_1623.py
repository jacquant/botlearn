# Generated by Django 3.0.3 on 2020-02-24 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_auto_20200224_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='parent',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, to='exercises.Section'),
        ),
    ]