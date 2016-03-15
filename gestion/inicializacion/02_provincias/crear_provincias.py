#!/usr/bin/env python3

from utilidades.basedatos.Configurador import Configurador
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *



with transaction.atomic():
    for tupla in Provincia.PROVINCIAS:
        (codigo, nombre)=tupla
        prov=Provincia(codigo)
        prov.save()
