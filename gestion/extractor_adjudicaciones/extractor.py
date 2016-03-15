#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD

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

nombramientos=Nombramiento.objects.all()
for nombramiento in nombramientos:
    cod_especialidad=nombramiento.especialidad.codigo_especialidad
    fecha_hoy=datetime.date(datetime.now())
    codigo_centro=nombramiento.centro.codigo_centro
    #print(codigo_centro)
    if i % max_filas == 0:
        nombre_funcion = prefijo_funcion + str(num_funcion)
        imprimir = GestorDB.get_procedimiento(nombre_funcion,
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
    
    fecha_inicio=utilidades.convertir_fecha_de_iso_a_estandar(fila[4])
    fecha_fin=utilidades.convertir_fecha_de_iso_a_estandar(fila[5])
    if fecha_hoy<fecha_final_contrato:
        descripcion_fechas = 'Desde ' + fecha_inicio + ' hasta ' + fecha_fin \
        + ' (' + fila[3] + ')'
    else:
        descripcion_fechas = 'En paro, su ultimo contrato acabó el ' + fecha_fin 
    temp = "update gaseosa set auxiliar='" + descripcion_fechas \
        + "' where dni='" + fila[0] + "'"
    sql_intermedio += GestorDB.crear_sentencia_update(temp)
    i = i + 1
nombre_funcion = prefijo_funcion + str(num_funcion)
imprimir = GestorDB.get_procedimiento(nombre_funcion, sql_intermedio)
print (imprimir)
num_funcion = num_funcion + 1
nombre_funcion = prefijo_funcion + str(num_funcion + 1)+"\r\n"
llamadas = 'Public Function ' + nombre_funcion.strip() + '()\r\n'
for num in range(1, num_funcion):
    llamadas += '\t' + prefijo_funcion + str(num) + '\r\n'
llamadas += 'End Function\r\n'
print (llamadas)

utilidades.anadir_a_fichero(nombre_funcion, 'llamadas_generales')
