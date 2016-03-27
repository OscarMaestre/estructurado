#!/usr/bin/env python3


import re
import sys
import string
import os




FECHA_NO_ENCONTRADA="Fecha no encontrada"


from utilidades.basedatos.Configurador import Configurador
from utilidades.fechas.GestorFechas import GestorFechas

import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

archivo=sys.argv[1]
re_dni="[0-9]{7,8}[A-Z]"
#especialidad="[PWB0]59[0-9][0-9]{3}"
re_especialidad="\- [PWB0]59([0-9]{4})"
re_codigo_centro="[0-9]{8}"
re_codigo_centro_ciudad_real="^13[0-9]{6}$"
re_fecha="[0-9]{2}/[0-9]{2}/[0-9]{4}"


gestor_fechas=GestorFechas()

def linea_contiene_patron(patron, linea):
    expresion=re.compile(patron)
    if expresion.search(linea):
        return True
    return False


def extraer_patron(patron, linea):
    expresion=re.compile(patron)
    concordancia=expresion.search(linea)
    if concordancia:
        inicio=concordancia.start()
        final=concordancia.end()
        return concordancia.string[inicio:final]
    return "No concordancia"



def extraer_codigo_centro(linea):
    return extraer_patron(re_codigo_centro, linea)

def extraer_localidad(linea):
    localidad=linea[9:51]
    return localidad.strip()

def extraer_dni(linea):
    trozo=linea[51:60]
    return extraer_patron(re_dni, linea)

def extraer_nombre(linea):
    linea=linea[49:]
    pos=string.find(linea, "-")
    if pos==-1:
        return "Error:"+linea
    return linea[pos+2:].strip()
    
    
cadena_sql="""insert into asignaciones_18092015 values
                    (
                        *C1*'{0}'*C1*,
                        *C2*'{1}'*C2*,
                        *C3*'{2}'*C3*,
                        *C4*'{3}'*C4*,
                        *C5*'{4}'*C5*,
                        *C6*'{5}'*C6*,
                        *C7*'{6}'*C7*,
                        *C8*'{7}'*C8*
                        
                    );
                    
                    """
           
def get_pos_comienzo_dni(linea, dni):
    return linea.find(dni)

def generar_linea_sql(lista_campos):
    dni=lista_campos[0]
    cod_centro=lista_campos[3]
    fecha_fin=lista_campos[7]
    if not linea_contiene_patron(re_codigo_centro_ciudad_real, cod_centro):
        cod_centro="9888"
    sql= "update gaseosa set cod_centro='"+cod_centro+"' where dni='"+dni+"';\n"
    sql+="update gaseosa set auxiliar='HACIENDO SUSTITUCION HASTA "+fecha_fin+"' where dni='"+dni+"';\n"
    return sql

def generar_linea_sql2(lista_campos):
    valores=":".join(lista_campos)
    return valores


def obtener_fecha_adjudicacion(linea):
    if (linea.find("CON COMIENZO ENTRE")==-1):
        return FECHA_NO_ENCONTRADA
    fecha=extraer_patron(re_fecha, linea[114:])
    trozos=fecha.split("/")
    dia=trozos[0]
    mes=trozos[1]
    anio=trozos[2]
    fecha="-".join([dia, mes, anio])
    return fecha

def es_jornada_completa(linea):
    if linea.find("JORNADA COMPLETA")!=-1:
        return True
    if linea.find("DE JORNADA")!=-1:
        return False
    return "TIPO DE JORNADA DESCONOCIDA"
    
def corregir_codigo_especialidad(codigo_especialidad, linea):
    if linea.find("INGLÉS")!=-1:
        if not es_jornada_completa(linea):
            nuevo_codigo="W"+codigo_especialidad[1:]
            return nuevo_codigo
        if es_jornada_completa(linea):
            nuevo_codigo="B"+codigo_especialidad[1:]
            return nuevo_codigo
    if linea.find("FRANCÉS")!=-1:
        if not es_jornada_completa(linea):
            nuevo_codigo="R"+codigo_especialidad[1:]
            return nuevo_codigo
        if es_jornada_completa(linea):
            nuevo_codigo="F"+codigo_especialidad[1:]
            return nuevo_codigo
    else:
        if not es_jornada_completa(linea):
            nuevo_codigo="P"+codigo_especialidad[1:]
            return nuevo_codigo
        if es_jornada_completa(linea):
            nuevo_codigo="0"+codigo_especialidad[1:]
            return nuevo_codigo
    


archivo=open(archivo,"r", encoding="utf-8")
lineas=archivo.readlines()
total_lineas=len(lineas)
codigo_especialidad=""
nombramientos=[]
fecha_adjudicacion=FECHA_NO_ENCONTRADA
fecha_adjudicacion_formato_iso=FECHA_NO_ENCONTRADA
procedimiento_adjudicacion=None
for i in range(0, total_lineas):

    linea=lineas[i]
    if fecha_adjudicacion==FECHA_NO_ENCONTRADA:
        fecha_adjudicacion=obtener_fecha_adjudicacion(linea)
        if (fecha_adjudicacion!=FECHA_NO_ENCONTRADA):
            fecha_adjudicacion_formato_iso=gestor_fechas.convertir_fecha_a_formato_iso(fecha_adjudicacion)
            procedimiento_adjudicacion=ProcedimientoAdjudicacion(
                nombre=ProcedimientoAdjudicacion.ASIGNACION_SUSTITUCIONES+ fecha_adjudicacion,
                fecha=fecha_adjudicacion_formato_iso
            )
            procedimiento_adjudicacion.save()
    if i+2==total_lineas:
        break
    linea_siguiente=lineas[i+1]
    linea_posterior=lineas[i+2]
    lista_campos=[]
    if (linea_contiene_patron(re_especialidad, linea)):
        codigo_especialidad=extraer_patron(re_especialidad, linea)
        codigo_especialidad=codigo_especialidad[2:]
    if (linea_contiene_patron(re_dni, linea)):
        dni=extraer_patron(re_dni, linea)
        
        nombre_centro=linea_posterior[0:26].strip()
        
        #Si es a media jornada un 0590004 se convierte en un P590004
        codigo_espe=corregir_codigo_especialidad(codigo_especialidad, linea_posterior)
        especialidad_asociada=Especialidad.objects.get ( codigo_especialidad=codigo_espe )
        pos_dni=get_pos_comienzo_dni(linea, dni)
        fin_dni=pos_dni+10
        nombre_persona=linea[fin_dni:fin_dni+40].strip()
        
        cod_centro=extraer_codigo_centro(linea[0:19])
        cod_centro=cod_centro + "C"
        #print (cod_centro)
        try:
            centro_asociado=Centro.objects.get( codigo_centro=cod_centro )
        except:
            print ("El centro {0} no parece existir!!!".format (cod_centro))
            continue
        
        nombre_localidad=linea[26:65].strip()
        fecha_inicio=extraer_patron(re_fecha, linea_posterior[111:141])
        fecha_fin=extraer_patron(re_fecha, linea_posterior[141:])
        fecha_inicio = gestor_fechas.convertir_fecha_a_formato_iso ( fecha_inicio )
        fecha_fin = gestor_fechas.convertir_fecha_a_formato_iso ( fecha_fin )
        nombre_persona=nombre_persona.replace("'", "-")
        nombramientos.append (
            (   dni,nombre_persona, especialidad_asociada,
                centro_asociado,fecha_inicio, fecha_fin )
        )
        
        continue
    else:
        continue
    
with transaction.atomic():
    for n in nombramientos:
        n=Nombramiento (
            nif = n[0],
            nombre_completo = n[1],
            centro = n[3],
            fecha_inicio =n[4],
            fecha_fin=n[5],
            proceso = procedimiento_adjudicacion,
            especialidad = n[2]
        )
        n.save()
    
    
archivo.close()
