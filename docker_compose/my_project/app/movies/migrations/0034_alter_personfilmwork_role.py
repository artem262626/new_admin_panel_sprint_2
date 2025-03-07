# Generated by Django 4.2.11 on 2025-01-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0033_alter_personfilmwork_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('director', 'Director'), ('actor', 'Actor'), ('producer', 'Producer'), ('screenwriter', 'Screenwriter'), ('actress', 'Actress'), ('cinematographer', 'Cinematographer'), ('editor', 'Editor'), ('production designer', 'Production Designer'), ('costumer', 'Costumer'), ('sound designer', 'Sound Designer'), ('gaffer', 'Gaffer')], max_length=255, verbose_name='role'),
        ),
    ]
