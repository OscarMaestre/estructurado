# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-21 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelado_bd', '0006_auto_20160421_0713'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentroOpos2016',
            fields=[
                ('codigo_centro', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('nombre_centro', models.CharField(max_length=60)),
                ('localidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Localidad')),
            ],
            options={
                'db_table': 'centros_opos_2016',
            },
        ),
    ]