#!/usr/bin/env python3
#coding=utf-8
from utilidades.basedatos.Configurador import Configurador
from utilidades.modelos.Modelos import get_directorio_archivos_especialidades,extraer_tuplas_especialidades_de_fichero
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..",".."]) )
configurador.activar_configuracion ( "gestion.settings")
from documentos.models import *

etiquetas=["boe", "docm", "instrucciones", "interinos", "retribuciones", "modelos"]
with transaction.atomic():
    for e in etiquetas:
        print ("Creando etiqueta "+e)
        eti=Etiqueta(valor=e)
        eti.save()
    