# Generated by Django 3.1.7 on 2021-09-02 05:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_france', '0030_indexs_recherche_elus'),
    ]

    operations = [
        migrations.AddField(
            model_name='canton',
            name='collectivite_departementale',
            field=models.ForeignKey(help_text='La collectivité pour laquelle ce canton sert de circonscription électorale.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cantons', related_query_name='canton', to='data_france.collectivitedepartementale', verbose_name='Collectivité départementale'),
        ),
        migrations.AddField(
            model_name='canton',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(geography=True, null=True, srid=4326, verbose_name='Géométrie'),
        ),
    ]
