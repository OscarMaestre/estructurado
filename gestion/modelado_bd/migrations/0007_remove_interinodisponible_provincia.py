# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-09 19:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelado_bd', '0006_auto_20160409_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interinodisponible',
            name='provincia',
        ),
    ]
