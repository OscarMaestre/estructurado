# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-04 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelado_bd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcionjornadas',
            name='enviado_email',
            field=models.BooleanField(default=False),
        ),
    ]