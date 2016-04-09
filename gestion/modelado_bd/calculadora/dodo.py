#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.Configurador import Configurador
from ProcesadorTablaDisponibles import ProcesadorTablaDisponibles
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *

from utilidades.ficheros.GestorFicheros import GestorFicheros
InterinoDisponible.objects.all().delete()

gf=GestorFicheros()
gf.ejecutar_comando ("./procesar2.py", "Ultima0590.pdf", "0590")