#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.Configurador import Configurador
from ProcesadorTablaDisponibles import ProcesadorTablaDisponibles
import sys
from django.db import connection

configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *

from utilidades.ficheros.GestorFicheros import GestorFicheros
InterinoDisponible.objects.all().delete()

TABLA_PROCEDIMIENTOS="procedimientos_adjudicacion"
TABLA_DISPONIBLES="interinos_disponibles"
TABLA_NOMBRAMIENTOS="nombramientos"
ultimo_proceso="""
    select nombre, fecha
        from {0}
        where nombre like 'Asigna%' and fecha in
            (
                select max(fecha) from {0}
            )
    """.format (TABLA_PROCEDIMIENTOS )

cursor = connection.cursor()
cursor.execute ( ultimo_proceso )
fila=cursor.fetchone()
nombre_ultima_asignacion=fila[0]
fecha_ultima_adjudicacion=fila[1]
#print (nombre_ultima_asignacion, fecha_ultima_adjudicacion)


gf=GestorFicheros()
gf.ejecutar_comando ("./procesar2.py", "Ultima0590.pdf", "0590")
gf.ejecutar_comando ("./procesar2.py", "Ultima0591.pdf", "0591")
gf.ejecutar_comando ("./procesar2.py", "Ultima0597.pdf", "0597")

#Se borran las personas que ya tienen nombramiento

borrado_ultimos="""
    delete from {0} where dni in
        (
            select nif from {1} where proceso_id='{2}'
        )
""".format (TABLA_DISPONIBLES, TABLA_NOMBRAMIENTOS, nombre_ultima_asignacion)
cursor.execute ( borrado_ultimos )
