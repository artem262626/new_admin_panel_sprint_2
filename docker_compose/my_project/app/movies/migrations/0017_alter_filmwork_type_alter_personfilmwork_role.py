# Generated by Django 4.2.11 on 2025-01-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_alter_filmwork_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='type',
            field=models.CharField(choices=[('Фильм', 'Movie'), ('ТВ Шоу', 'Tv Show'), ('Сериал', 'Serial'), ('Мультфильм', 'Multfilm')], default='Фильм', max_length=10),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(max_length=100, verbose_name='role'),
        ),
    ]
