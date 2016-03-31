#!/usr/bin/env python3

import os, sys, re

NUM_SUBDIRECTORIOS_ANTERIORES=1
SEPARADOR=os.sep

RUTA_PAQUETE_BD=(".."+SEPARADOR) * NUM_SUBDIRECTORIOS_ANTERIORES
DIRECTORIO= RUTA_PAQUETE_BD + os.sep+"Verano"+os.sep+"db_nombramientos"
#aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIRECTORIO)
import GestorDB
import utilidades
import ListaCampos


gestorbd=GestorDB.BD_RESULTADOS

TABLA_ESPECIALIDADES=utilidades.NOMBRE_TABLA_ESPECIALIDADES
PROCEDIMIENTO_PRACTICAS="Nombramiento EEMM en practicas para 15/16"

codigos_especialidad=gestorbd.get_filas(
    "select especialidad, descripcion from {0}".format(TABLA_ESPECIALIDADES)
)

SQL_PRACTICAS="""
    select count(*) from nombramientos where procedimiento='{0}'
        and
            especialidad='{1}'
"""
for elem in codigos_especialidad:
   codigo=elem[0]
   descr=elem[1]
   sql_cuantos_en_practicas=SQL_PRACTICAS.format(PROCEDIMIENTO_PRACTICAS, codigo)
   cuantos_en_practicas=gestorbd.get_filas(sql_cuantos_en_practicas)
   cantidad=cuantos_en_practicas[0][0]
   if cantidad==0:
        continue
   informe_practicas="Especialidad:{0} Cantidad en practicas{1}".format(
        descr, cantidad
   )
   print (informe_practicas)
    
    