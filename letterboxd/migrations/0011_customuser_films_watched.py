# Generated by Django 3.2.8 on 2021-12-07 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letterboxd', '0010_addfilm'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='films_watched',
            field=models.ManyToManyField(to='letterboxd.Film'),
        ),
    ]
