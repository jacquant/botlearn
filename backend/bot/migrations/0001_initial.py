from django.db import (
    migrations,
    models,
)

import ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.TextField(verbose_name='question type (pas de ponctuation,majuscule)')),

                ('matched', models.BooleanField(default=True, verbose_name='possède une réponse associée')),
                ('asked', models.IntegerField(default=1, verbose_name='nombre de fois que la question a été posée')),
            ],
            options={
                'ordering': ['intitule'],
            },
        ),
        migrations.CreateModel(
            name='Reponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse', ckeditor.fields.RichTextField()),
                ('question', models.ManyToManyField(to='bot.Question')),
            ],
        ),
    ]
