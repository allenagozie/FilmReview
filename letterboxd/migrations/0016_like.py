# Generated by Django 3.2.8 on 2021-12-08 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('letterboxd', '0015_alter_following_the_followed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('films', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterboxd.film')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
