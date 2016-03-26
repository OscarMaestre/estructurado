#!/usr/bin/env python3


import re
import sys
import os
from utilidades.basedatos.Configurador import Configurador
from utilidades.fechas.GestorFechas import GestorFechas
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
re_codigo_localidad="[0-9]{9}"
re_codigo_centro_ciudad_real="^13[0-9]{6}$"
re_fecha="[0-9]{2}/[0-9]{2}/[0-9]{4}"

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
    print ("No concordancia")



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
    pos=linea.find("-")
    if pos==-1:
        return "Error:"+linea
    return linea[pos+2:].strip()
 
def get_localidad( cod_localidad, nom_localidad):
    inicio_prov=cod_localidad[0:2]
    zona_asociada=Zona.objects.get(codigo_zona=Zona.ZONA_CLM)
    print (inicio_prov)
    provs={
        "13":"CR",
        "02":"AB",
        "45":"TO",
        "19":"GU",
        "16":"CU"
    }
    prov_asociada=Provincia.objects.get(provincia=provs[inicio_prov])
    localidad=Localidad (
                codigo_localidad=cod_localidad,
                nombre_localidad=nom_localidad,
                provincia=prov_asociada,
                zona=zona_asociada
    )
    localidad.save()
    return localidad   
    

archivo=open(archivo,"r", encoding="utf-8")
lineas=archivo.readlines()
total_lineas=len(lineas)
codigo_especialidad=""
procedimiento_adjudicacion=ProcedimientoAdjudicacion(
    nombre=ProcedimientoAdjudicacion.VACANTES_18_09_2015, fecha="2015-09-18")
procedimiento_adjudicacion.save()
gestor_fechas=GestorFechas()
nombramientos=[]
for i in range(0, total_lineas):
    linea=lineas[i]
    if (linea_contiene_patron(re_especialidad, linea)):
        codigo_espe=extraer_patron(re_especialidad, linea)
        codigo_espe=codigo_espe[2:]
    if (linea_contiene_patron(re_dni, linea)):
        linea_limpia=linea.strip()
        cod_localidad=extraer_patron(re_codigo_localidad, linea)
        nom_localidad=linea[16:53].strip()
        cod_centro=extraer_codigo_centro(linea_limpia)
        #Todos los centros de nuestra BD llevan C al final, pero
        #en esta adjudicación no lo han puesto. Lo añadimos a mano
        cod_centro+="C"
        localidad=extraer_localidad(linea_limpia)
        
        dni = extraer_dni(linea_limpia)
        
        nombre = extraer_nombre(linea_limpia)
        
        linea_siguiente=lineas[i+1]
        nom_centro=linea_siguiente[0:51].strip()
        trozo_fecha1=linea_siguiente[72:132]
        fecha_1=extraer_patron(re_fecha, trozo_fecha1)
        trozo_fecha2=linea_siguiente[133:]
        fecha_2=extraer_patron(re_fecha, trozo_fecha2)
        fecha_1=gestor_fechas.convertir_fecha_a_formato_iso(fecha_1)
        fecha_2=gestor_fechas.convertir_fecha_a_formato_iso(fecha_2)
        
        especialidad_asociada=Especialidad.objects.get ( codigo_especialidad=codigo_espe )
        try:
            centro_asociado=Centro.objects.get( codigo_centro=cod_centro )
        except:
            print ("No existe el centro {0}".format(cod_centro))
            loc_asociada=get_localidad (cod_localidad, nom_localidad)
            centro_asociado=Centro(
                codigo_centro=cod_centro, nombre_centro=nom_centro,
                localidad=loc_asociada
            )
            centro_asociado.save()
        
        
        nombramientos.append(
            (
                dni, nombre, especialidad_asociada, centro_asociado,
                fecha_1, fecha_2
            )
        )        
        #print cadena_sql.format(codigo_especialidad, codigo_centro, localidad, dni, nombre, nombre_centro, fecha_1, fecha_2)
        i=i+1
        

