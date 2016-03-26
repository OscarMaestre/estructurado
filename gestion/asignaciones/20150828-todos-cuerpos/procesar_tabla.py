#!/usr/bin/env python3
#coding=utf-8

import re
import sys
import string
import os
from datetime import date

from utilidades.basedatos.Configurador import Configurador
from utilidades.fechas.GestorFechas import GestorFechas

import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

procedimiento_adjudicacion=ProcedimientoAdjudicacion(
    nombre=ProcedimientoAdjudicacion.VACANTES_28_08_2015, fecha="2015-08-28")
procedimiento_adjudicacion.save()

archivo=sys.argv[1]
re_dni="[0-9]{7,8}[A-Z]"
#especialidad="[PWB0]59[0-9][0-9]{3}"
re_especialidad="[FRPWB0]59([0-9]{4})"
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
def generar_linea_sql(lista_campos):
    dni=lista_campos[0]
    cod_centro=lista_campos[3]
    if not linea_contiene_patron(re_codigo_centro_ciudad_real, cod_centro):
        cod_centro="9888"
    sql= "update gaseosa set cod_centro='"+cod_centro+"' where dni='"+dni+"';\n"
    sql+="update gaseosa set auxiliar='VACANTE TODO CURSO 15/16' where dni='"+dni+"';\n"
    return sql
                                        
def generar_linea_sql2(lista_campos):
    valores=":".join(lista_campos)
    return valores

def get_localidad( cod_localidad, nom_localidad):
    try:
        loc=Localidad.objects.get(codigo_localidad=cod_localidad)
        return loc
    except:
        pass
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
nombramientos=[]

for i in range(0, total_lineas):
    linea=lineas[i]
    if i+1==total_lineas:
        break
    linea_siguiente=lineas[i+1]
    if (linea_contiene_patron(re_dni, linea_siguiente)):
        dni=extraer_patron(re_dni, linea_siguiente)
        
        nom_centro=linea_siguiente[28:61].strip()
        
        nombre_persona=linea[:32].strip()
        
        cod_centro=extraer_codigo_centro(linea[27:64])
        #Los codigos de centro de esta adjudicacion no llevan C, se la añadimos
        cod_centro+="C"
        codigo_espe=extraer_patron(re_especialidad, linea[49:86])
        cod_localidad=extraer_patron(re_codigo_localidad, linea)
        #print (cod_localidad)
        nom_localidad=linea_siguiente[94:].strip()
        especialidad_asociada=Especialidad.objects.get ( codigo_especialidad=codigo_espe )
        try:
            centro_asociado=Centro.objects.get( codigo_centro=cod_centro )
        except:
            loc_asociada=get_localidad (cod_localidad, nom_localidad)
            centro_asociado=Centro(
                codigo_centro=cod_centro, nombre_centro=nom_centro,
                localidad=loc_asociada
            )
            centro_asociado.save()
            
            print ("No existe el centro {0}".format(cod_centro))
            
        
        nombramientos.append (
            (
                dni, nombre_persona, especialidad_asociada,
                centro_asociado, "2015-09-01", "2016-06-24"
            )
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

