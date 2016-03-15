# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-14 22:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('codigo_centro', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('nombre_centro', models.CharField(max_length=60)),
                ('tipo_centro', models.CharField(choices=[('CEIP', '(CEIP) Colegio de primaria'), ('CEE', '(CEE) Centro de Educaci\xf3n Especial'), ('CRA', '(CRA) Centro Rural Agrupado'), ('IESO', '(IESO) Instituto de ESO'), ('IES', '(IES) Instituto de Educaci\xf3n Secundaria'), ('CIPFPU', '(CIPFPU) Centro Integrado de FP'), ('Cifppu', '(CIPFPU) Centro Integrado de FP'), ('Ifp', '(IFP) Centro Integrado de FP'), ('CPM', '(CPM) Conservatorio Profesional de M\xfasica'), ('CPD', '(CPM) Conservatorio Profesional de Danza'), ('SES', '(SES) Secci\xf3n de Educaci\xf3n Secundaria'), ('EA', '(EA) Escuela de Artes'), ('EOI', '(EOI) Escuela Oficial de Idiomas'), ('CEPA', '(CEPA) Centro Educaci\xf3n Personas Adultas'), ('AEPA', '(AEPA) Aul Educaci\xf3n Personas Adultas'), ('DESC', '(DESC) Desconocido')], max_length=12)),
            ],
            options={
                'db_table': 'centros',
            },
        ),
        migrations.CreateModel(
            name='DireccionesCentro',
            fields=[
                ('codigo_centro', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('naturaleza', models.CharField(max_length=20)),
                ('nombre_centro', models.CharField(max_length=100)),
                ('direccion_postal', models.CharField(max_length=120)),
                ('codigo_postal', models.CharField(max_length=6)),
                ('tlf', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=15)),
                ('web', models.CharField(max_length=160)),
            ],
            options={
                'db_table': 'direcciones_centros',
            },
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('codigo_especialidad', models.CharField(db_index=True, max_length=8, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=80)),
                ('idioma', models.CharField(max_length=15)),
                ('tipo_de_jornada', models.CharField(choices=[('COMPLETA', 'Jornada Completa'), ('MEDIA JORNADA', 'Media jornada'), ('TERCIO DE JORNADA', 'Tercio de Jornada')], max_length=40)),
            ],
            options={
                'db_table': 'especialidades',
            },
        ),
        migrations.CreateModel(
            name='Gaseosa',
            fields=[
                ('dni', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('cuota', models.CharField(blank=True, max_length=10, null=True)),
                ('apellido_1', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('apellido_2', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, max_length=60, null=True)),
                ('sexo', models.CharField(blank=True, max_length=2, null=True)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=6, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('provincia', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('tlf_casa', models.CharField(blank=True, max_length=18, null=True)),
                ('tlf_movil', models.CharField(blank=True, max_length=18, null=True)),
                ('fecha_alta', models.DateField(blank=True, null=True)),
                ('fecha_baja', models.DateField(blank=True, null=True)),
                ('cuerpo', models.CharField(blank=True, max_length=10, null=True)),
                ('cod_centro_def', models.CharField(blank=True, max_length=12, null=True)),
                ('cod_centro_actual', models.CharField(blank=True, db_index=True, max_length=12, null=True)),
                ('auxiliar', models.TextField(blank=True, max_length=2048, null=True)),
                ('iban', models.CharField(blank=True, max_length=4, null=True)),
                ('ccc', models.CharField(blank=True, max_length=20, null=True)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Especialidad')),
            ],
            options={
                'ordering': ['apellido_1', 'apellido_2', 'nombre'],
                'db_table': 'gaseosa',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('codigo_localidad', models.CharField(db_index=True, max_length=12, primary_key=True, serialize=False)),
                ('nombre_localidad', models.CharField(max_length=80)),
                ('latitud', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
                ('longitud', models.DecimalField(decimal_places=8, default=0.0, max_digits=11)),
            ],
            options={
                'db_table': 'localidades',
            },
        ),
        migrations.CreateModel(
            name='LocalidadAsociadaCRA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_localidad', models.CharField(max_length=50)),
                ('cra_cabecera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Centro')),
            ],
            options={
                'db_table': 'localidades_de_cra',
            },
        ),
        migrations.CreateModel(
            name='Nombramiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nif', models.CharField(max_length=12)),
                ('nombre_completo', models.CharField(max_length=180)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('auxiliar', models.CharField(max_length=240)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Centro')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Especialidad')),
            ],
            options={
                'db_table': 'nombramientos',
            },
        ),
        migrations.CreateModel(
            name='ProcedimientoAdjudicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'procedimientos_adjudicacion',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('provincia', models.CharField(choices=[('CR', 'Ciudad Real'), ('AB', 'Albacete'), ('GU', 'Guadalajara'), ('TO', 'Toledo'), ('CU', 'Cuenca')], max_length=4, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'provincias',
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('codigo_zona', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'zonas',
            },
        ),
        migrations.AddField(
            model_name='nombramiento',
            name='proceso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.ProcedimientoAdjudicacion'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Provincia'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Zona'),
        ),
        migrations.AddField(
            model_name='direccionescentro',
            name='codigo_localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Localidad'),
        ),
        migrations.AddField(
            model_name='centro',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Localidad'),
        ),
    ]
