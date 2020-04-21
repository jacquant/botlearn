# Generated by Django 3.0.5 on 2020-04-21 08:00

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20200406_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='question',
            old_name='intitule',
            new_name='title',
        ),
        migrations.DeleteModel(
            name='Reponse',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ManyToManyField(to='bot.Question'),
        ),
    ]
