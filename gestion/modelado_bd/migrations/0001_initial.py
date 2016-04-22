# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-22 17:37
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
                ('tipo_centro', models.CharField(choices=[('CEIP', '(CEIP) Colegio de primaria'), ('CEE', '(CEE) Centro de Educación Especial'), ('CRA', '(CRA) Centro Rural Agrupado'), ('IESO', '(IESO) Instituto de ESO'), ('IES', '(IES) Instituto de Educación Secundaria'), ('CIPFPU', '(CIPFPU) Centro Integrado de FP'), ('Cifppu', '(CIPFPU) Centro Integrado de FP'), ('Ifp', '(IFP) Centro Integrado de FP'), ('CPM', '(CPM) Conservatorio Profesional de Música'), ('CPD', '(CPM) Conservatorio Profesional de Danza'), ('SES', '(SES) Sección de Educación Secundaria'), ('EA', '(EA) Escuela de Artes'), ('EOI', '(EOI) Escuela Oficial de Idiomas'), ('CEPA', '(CEPA) Centro Educación Personas Adultas'), ('AEPA', '(AEPA) Aul Educación Personas Adultas'), ('UO', '(UO) Unidad de Orientacion'), ('DP', '(DP) Delegación Provincial de Educación'), ('DESC', '(DESC) Desconocido')], max_length=12)),
                ('naturaleza', models.CharField(choices=[('Público', 'Público'), ('Privado', 'Privado'), ('Concertado', 'Concertado'), ('Desconocida', 'Desconocida')], default='Público', max_length=15)),
            ],
            options={
                'db_table': 'centros',
            },
        ),
        migrations.CreateModel(
            name='CentroOpos2016',
            fields=[
                ('codigo_centro', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('nombre_centro', models.CharField(max_length=60)),
            ],
            options={
                'db_table': 'centros_opos_2016',
            },
        ),
        migrations.CreateModel(
            name='DireccionesCentro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion_postal', models.CharField(max_length=120)),
                ('codigo_postal', models.CharField(max_length=6)),
                ('tlf', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=160)),
                ('web', models.CharField(max_length=160)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Centro')),
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
                'verbose_name_plural': 'especialidades',
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
                ('auxiliar', models.TextField(blank=True, max_length=2048, null=True)),
                ('iban', models.CharField(blank=True, max_length=4, null=True)),
                ('ccc', models.CharField(blank=True, max_length=20, null=True)),
                ('cod_centro_actual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centro_actual', to='modelado_bd.Centro')),
                ('cod_centro_def', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centro_definitivo', to='modelado_bd.Centro')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Especialidad')),
            ],
            options={
                'db_table': 'gaseosa',
                'ordering': ['apellido_1', 'apellido_2', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='GaseoWeb',
            fields=[
                ('dni', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('apellido_1', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('apellido_2', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'db_table': 'web',
            },
        ),
        migrations.CreateModel(
            name='InscripcionJornadas',
            fields=[
                ('id_inscripcion', models.IntegerField(primary_key=True, serialize=False)),
                ('nif', models.CharField(blank=True, max_length=12, null=True)),
                ('apellido1', models.CharField(max_length=60)),
                ('apellido2', models.CharField(max_length=60)),
                ('nombre', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
                ('anios_exp', models.IntegerField()),
                ('especialidad', models.CharField(max_length=30)),
                ('afiliado', models.CharField(max_length=10)),
                ('pago', models.CharField(choices=[('Por procesar', 'Por procesar'), ('Efectivo', 'Pagado en efectivo'), ('Transferencia', 'Pagado por transf'), ('No pagado', 'No pagado'), ('Descartada', 'Descartada')], max_length=20)),
                ('confirmada', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'inscripciones_jornadas',
                'ordering': ['apellido1', 'apellido2'],
            },
        ),
        migrations.CreateModel(
            name='InterinoDisponible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField()),
                ('dni', models.CharField(max_length=12)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('tipo_bolsa', models.CharField(choices=[('0', 'Bolsa 0'), ('1', 'Bolsa 1'), ('2D', 'Bolsa 2D'), ('2F', 'Bolsa 2F'), ('2H', 'Bolsa 2H'), ('2J', 'Bolsa 2J'), ('2K', 'Bolsa 2K'), ('2L', 'Bolsa 2L'), ('2M', 'Bolsa 2M'), ('3H', 'Bolsa 3H'), ('3G', 'Bolsa 3G'), ('2', 'Bolsa 2'), ('3', 'Bolsa 3'), ('4F', 'Bolsa 4F'), ('4', 'Bolsa 4'), ('6M', 'Bolsa 6M'), ('6', 'Bolsa 6'), ('7G', 'Bolsa 7G'), ('7P', 'Bolsa 7P'), ('7J', 'Bolsa 7J'), ('8', 'Bolsa 8'), ('P0', 'Bolsa P0'), ('P1B', 'Bolsa P1B'), ('P1', 'Bolsa P1'), ('P2', 'Bolsa P2'), ('P4', 'Bolsa P4'), ('R1', 'Bolsa R1'), ('2N', 'Bolsa 2N'), ('4E', 'Bolsa 4E'), ('4G', 'Bolsa 4G'), ('R1H', 'Bolsa R1H'), ('R1F', 'Bolsa R1F'), ('R1D', 'Bolsa R1D'), ('R1G', 'Bolsa R1G'), ('R1I', 'Bolsa R1I')], max_length=10)),
                ('orden_bolsa', models.IntegerField()),
                ('ingles', models.BooleanField()),
                ('frances', models.BooleanField()),
                ('elige_ab', models.BooleanField(default=False)),
                ('elige_cr', models.BooleanField(default=False)),
                ('elige_cu', models.BooleanField(default=False)),
                ('elige_gu', models.BooleanField(default=False)),
                ('elige_to', models.BooleanField(default=False)),
                ('especialidad', models.ManyToManyField(to='modelado_bd.Especialidad')),
            ],
            options={
                'db_table': 'interinos_disponibles',
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
            name='LocalidadOpos2016',
            fields=[
                ('codigo_localidad', models.CharField(db_index=True, max_length=12, primary_key=True, serialize=False)),
                ('nombre_localidad', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'localidades_opos_2016',
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
                ('nombre', models.CharField(max_length=150, primary_key=True, serialize=False)),
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
            name='ProvinciaOpos2016',
            fields=[
                ('codigo_provincia', models.CharField(db_index=True, max_length=15, primary_key=True, serialize=False)),
                ('nombre_provincia', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='RutaOpos2016',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distancia', models.IntegerField()),
                ('minutos', models.IntegerField()),
                ('sumario', models.CharField(max_length=250)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loc_destino', to='modelado_bd.LocalidadOpos2016')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loc_origen', to='modelado_bd.LocalidadOpos2016')),
            ],
            options={
                'db_table': 'rutas',
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
            model_name='localidadopos2016',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.ProvinciaOpos2016'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Provincia'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='zona',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Zona'),
        ),
        migrations.AddField(
            model_name='direccionescentro',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Localidad'),
        ),
        migrations.AddField(
            model_name='centroopos2016',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.LocalidadOpos2016'),
        ),
        migrations.AddField(
            model_name='centro',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelado_bd.Localidad'),
        ),
    ]
