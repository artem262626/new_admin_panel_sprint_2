# Generated by Django 4.2.11 on 2025-01-12 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0032_filmwork_film_work_creatio_02a6ad_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('director', 'director'), ('actor', 'actor')], max_length=255, verbose_name='role'),
        ),
    ]
