# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 12:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0005_fichero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fichero',
            name='nombre',
        ),
        migrations.AddField(
            model_name='fichero',
            name='archivo',
            field=models.FileField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fichero',
            name='fecha_documento',
            field=models.DateField(default=datetime.datetime(2016, 3, 24, 12, 16, 0, 498357, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fichero',
            name='fecha_publicacion',
            field=models.DateField(default=datetime.datetime(2016, 3, 24, 12, 16, 8, 362927, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
