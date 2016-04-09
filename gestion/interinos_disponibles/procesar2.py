#!/usr/bin/env python3
# coding=utf-8



from utilidades.basedatos.Configurador import Configurador
from ProcesadorTablaDisponibles import ProcesadorTablaDisponibles
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
fichero=sys.argv[1]
codigo_cuerpo_cuatro_digitos=sys.argv[2] # Por ejemplo 0590, 0597
procesador=ProcesadorTablaDisponibles(
    fichero, InterinoDisponible,
    codigo_cuerpo_cuatro_digitos, InterinoDisponible, Especialidad )

procesador.procesar_tabla()