# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0004_auto_20160324_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fichero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=240)),
                ('fecha_subida', models.DateField()),
                ('etiquetas', models.ManyToManyField(to='documentos.Etiqueta')),
            ],
        ),
    ]
