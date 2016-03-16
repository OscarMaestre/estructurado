#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
from utilidades.fechas.GestorFechas import GestorFechas
from utilidades.ficheros.GestorFicheros import GestorFicheros

import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join ([".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

from datetime import datetime


i=1
max_filas=300
sql_intermedio=""

sufijo_fecha = sys.argv[1]
sufijo_fecha = sufijo_fecha.replace('-', '')
prefijo_funcion = 'fun_' + sufijo_fecha + '_'
num_funcion=1

nombramientos=Nombramiento.objects.all()
for nombramiento in nombramientos:
    cod_especialidad=nombramiento.especialidad.codigo_especialidad
    fecha_hoy=datetime.date(datetime.now())
    codigo_centro=nombramiento.centro.codigo_centro
    #print(codigo_centro)
    if i % max_filas == 0:
        nombre_funcion = prefijo_funcion + str(num_funcion)
        imprimir = GestorBD.get_procedimiento(nombre_funcion,
                sql_intermedio)
        print (imprimir)
        num_funcion = num_funcion + 1

        sql_intermedio = ''
        
    if fecha_hoy>nombramiento.fecha_fin:
        if cod_especialidad.find("597")!=-1:
            codigo_centro="9999"
        else:
            codigo_centro="9998"
    lista_registros = []
    
    # temp="update gaseosa set codcentrodefinitivo='"+fila[2]+"' where dni='"+fila[0]+"'"
    # sql_intermedio+= (GestorDB.crear_sentencia_update(temp))

    temp = "update gaseosa set codcentrocursoactual='" + codigo_centro \
        + "' where dni='" + nombramiento.nif + "'"
    sql_intermedio += GestorBD.crear_sentencia_update(temp)
    
    fecha_inicio    =   nombramiento.fecha_inicio
    fecha_fin       =   nombramiento.fecha_fin 
    if fecha_hoy<fecha_fin:
        descripcion_fecha_inicio=nombramiento.fecha_inicio.strftime("%d-%m-%Y")
        descripcion_fecha_fin   =nombramiento.fecha_fin.strftime("%d-%m-%Y")
        descripcion_fechas = 'Desde ' + descripcion_fecha_inicio + \
                             ' hasta ' + descripcion_fecha_fin \
        + ' (' + nombramiento.especialidad.descripcion + ')'
    else:
        descripcion_fecha_fin=fecha_fin.strftime("%d-%m-%Y")
        descripcion_fechas = 'En paro, su ultimo contrato acabó el ' + descripcion_fecha_fin
    temp = "update gaseosa set auxiliar='" + descripcion_fechas \
        + "' where dni='" + nombramiento.nif + "'"
    sql_intermedio += GestorBD.crear_sentencia_update(temp)
    i = i + 1
nombre_funcion = prefijo_funcion + str(num_funcion)
imprimir = GestorBD.get_procedimiento(nombre_funcion, sql_intermedio)
print (imprimir)
num_funcion = num_funcion + 1
nombre_funcion = prefijo_funcion + str(num_funcion + 1)+"\r\n"
llamadas = 'Public Function ' + nombre_funcion.strip() + '()\r\n'
for num in range(1, num_funcion):
    llamadas += '\t' + prefijo_funcion + str(num) + '\r\n'
llamadas += 'End Function\r\n'
print (llamadas)

gestor_ficheros=GestorFicheros()
gestor_ficheros.anadir_a_fichero(nombre_funcion, 'llamadas_generales')
