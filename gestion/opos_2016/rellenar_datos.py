#!/usr/bin/env python3
# coding=utf-8



from utilidades.basedatos.Configurador import Configurador
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *

fichero=sys.argv[1]


RutaOpos2016.objects.all().delete()
LocalidadOpos2016.objects.all().delete()
ProvinciaOpos2016.objects.all().delete()
