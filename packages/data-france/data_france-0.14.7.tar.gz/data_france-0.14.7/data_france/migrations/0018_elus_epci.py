# Generated by Django 3.1.6 on 2021-02-08 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_france", "0017_mairies"),
    ]

    operations = [
        migrations.AddField(
            model_name="elumunicipal",
            name="date_debut_fonction_epci",
            field=models.DateField(
                editable=False,
                null=True,
                verbose_name="Date de début de la fonction auprès de l'EPCI",
            ),
        ),
        migrations.AddField(
            model_name="elumunicipal",
            name="date_debut_mandat_epci",
            field=models.DateField(
                editable=False,
                null=True,
                verbose_name="Date de début du mandat auprès de l'EPCI",
            ),
        ),
        migrations.AddField(
            model_name="elumunicipal",
            name="fonction_epci",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=60,
                verbose_name="Fonction auprès de l'EPCI",
            ),
        ),
    ]
