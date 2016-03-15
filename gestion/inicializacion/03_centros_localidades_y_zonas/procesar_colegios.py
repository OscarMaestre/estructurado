#!/usr/bin/env python3
#coding=utf-8

import sys, re
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.cadenas.procesamientocadenas import *
from utilidades.internet.internet import get_latitud_longitud


from utilidades.basedatos.Configurador import Configurador
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *





RE_CALLE="(Cl\.|Cm\.|Av\.|Pq\.|Pz\.|Cj\.|Ps\.|Cr\.|Tr\.|Rd\.|Gl\.|Ct\.|Ur\.)"
EXP_REG_CALLE=re.compile ( RE_CALLE )
        
RE_COD_POSTAL=" [0-9]{5} "
EXPR_REG_COD_POSTAL=re.compile ( RE_COD_POSTAL )

RE_COD_ZONA=" [0-9]{6}$"
EXPR_REG_COD_ZONA=re.compile ( RE_COD_ZONA )
        
def extraer_nombre_centro ( procesador_pdf, fin_cod_centro ):
    linea_actual=procesador_pdf.get_linea_actual()
    (ini_nombre_centro, fin_nombre_centro, texto_ini_colegio)=procesador_pdf.linea_contiene_patron(
                EXP_REG_CALLE, linea_actual  )
    nombre_centro=linea_actual[fin_cod_centro:ini_nombre_centro].strip()
    nombre_centro=quitar_pueblo_entre_parentesis(nombre_centro)
    nombre_centro=corregir_vi(nombre_centro)
    return nombre_centro

def get_posicion_codigo_postal(procesador_pdf):
    linea_actual=procesador_pdf.get_linea_actual()
    (ini_cp, fin_cp, cp)=procesador_pdf.linea_contiene_patron(
                EXPR_REG_COD_POSTAL, linea_actual  )
    return ini_cp-1



def extraer_nombre_localidad(procesador_pdf, fin_cod_localidad):
    pos_cp=get_posicion_codigo_postal(procesador_pdf)
    linea_actual=procesador_pdf.get_linea_actual()
    linea_con_loc_repetidas=linea_actual[fin_cod_localidad:pos_cp].strip()
    pos_espacios=linea_con_loc_repetidas.find("   ")
    localidad=linea_con_loc_repetidas[:pos_espacios].strip()
    return localidad
    
    
def establecer_provincia(procesador_pdf, provincia_anterior):
    CODIGOS_ASOCIADOS={
        "Toledo":"TO",
        "Ciudad Real":"CR",
        "Cuenca":"CU",
        "Albacete":"AB",
        "Guadalajara":"GU"
    }
    linea_actual=procesador_pdf.get_linea_actual()
    pos_cad_provincia=linea_actual.find( "Provincia " )
    if (pos_cad_provincia==-1):
        return provincia_anterior
    prov=linea_actual[pos_cad_provincia+10:].strip()
    print ("Examinando centros de provincia:"+prov+"-")
    return CODIGOS_ASOCIADOS[prov]
    
def get_localidades_asociadas(procesador_pdf):
    localidades_asociadas=[]
    linea_actual=procesador_pdf.get_linea_actual()
    if linea_actual.find("Localidades del ")!=-1:
        print ("CRA con localidades asociadas")
        procesador_pdf.siguiente_linea()
        linea_actual=procesador_pdf.get_linea_actual()
        while len(linea_actual)>2:
            #print (linea_actual)
            localidades_asociadas.append (  linea_actual.strip() )
            procesador_pdf.siguiente_linea()
            linea_actual=procesador_pdf.get_linea_actual()
        #Fin del while
        #print (localidades_asociadas)
    return localidades_asociadas

def crear_entidades(procesador_pdf):
    """Se mueve a través del fichero TXT creando los centros, localidades y zonas de los colegios"""
    codigos_pueblos_ya_buscados=[]
    zonas=[]
    localidades=[]
    centros=[]
    provincia_actual=""
    ultima_latitud=0
    ultima_longitud=0
    latitud=0
    longitud=0
    localidades_asociadas_a_cra=[]
    ultimo_codigo_centro_valido=""
    while not procesador_pdf.eof():
        provincia_actual=establecer_provincia(procesador_pdf, provincia_actual)
        linea_actual=procesador_pdf.get_linea_actual()
        (ini_cod_centro, fin_cod_centro, codigo_centro) = procesador_pdf.linea_contiene_patron(
            procesador_pdf.expr_regular_codigo_centro_con_c, linea_actual
        )
        if codigo_centro!=procesador_pdf.PATRON_NO_ENCONTRADO:
            ultimo_codigo_centro_valido=codigo_centro
            nombre_centro = extraer_nombre_centro ( procesador_pdf , fin_cod_centro)
            (ini_cod_loc, fin_cod_loc, codigo_localidad)=procesador_pdf.linea_contiene_patron(
                procesador_pdf.expr_regular_codigo_localidad, linea_actual
            )
            nombre_localidad=extraer_nombre_localidad ( procesador_pdf, fin_cod_loc )
            #if codigo_localidad not in codigos_pueblos_ya_buscados:
            #    (latitud, longitud) = get_latitud_longitud ( nombre_localidad )
            #    ultima_latitud=latitud
            #    ultima_longitud=longitud
            #    codigos_pueblos_ya_buscados.append ( codigo_localidad )
            #else:
            #    latitud=ultima_latitud
            #    longitud=ultima_longitud
            (ini_zona, fin_zona, codigo_zona)=procesador_pdf.linea_contiene_patron (
                EXPR_REG_COD_ZONA, linea_actual
            )
            codigo_zona=codigo_zona.strip()
            zonas.append ( codigo_zona )
            localidades.append  (
                (codigo_localidad, nombre_localidad,
                 codigo_zona, provincia_actual, latitud, longitud )
            )
            print (codigo_centro, ">>"+nombre_centro+"<<", codigo_localidad, ">>"+nombre_localidad+"<<", codigo_zona, provincia_actual)
            centros.append ( (codigo_centro, nombre_centro, codigo_localidad))
        else:
            localidades_de_cra=get_localidades_asociadas(procesador_pdf)
            if localidades_de_cra!=[]:
                for l in localidades_de_cra:
                    localidades_asociadas_a_cra.append ( (ultimo_codigo_centro_valido, l) )
        procesador_pdf.siguiente_linea()
    #Fin del while
    #Añadimos las zonas
    with transaction.atomic():
        for z in zonas:
            zona=Zona(codigo_zona=z)
            zona.save()
    with transaction.atomic():
        for l in localidades:
            #print (l)
            zona_asociada=Zona.objects.get(pk=l[2])
            provincia_asociada=Provincia.objects.get(pk=l[3])
            
            #print (zona_asociada.codigo_zona)
            localidad=Localidad ( codigo_localidad=l[0], nombre_localidad=l[1],
                                 zona=zona_asociada, provincia=provincia_asociada,
                                 latitud=l[4], longitud=l[5])
            localidad.save()
    with transaction.atomic():
        for c in centros:
            cod_loc_asociada=c[2]
            localidad_asociada=Localidad.objects.get(codigo_localidad=cod_loc_asociada)
            centro=Centro ( codigo_centro = c[0], nombre_centro=c[1], localidad=localidad_asociada)
            centro.save()
    with transaction.atomic():
        #print (localidades_asociadas_a_cra)
        for l in localidades_asociadas_a_cra:
            cra=Centro.objects.get ( pk=l[0] )
            localidad_de_cra=LocalidadAsociadaCRA ( cra_cabecera = cra, nombre_localidad=l[1])
            localidad_de_cra.save()
        
if __name__ == '__main__':
    procesador_pdf=ProcesadorPDF()
    try:
        procesador_pdf.abrir_fichero_txt ( sys.argv[1] )
        crear_entidades(procesador_pdf)
    except IndexError:
        print ("Indique el nombre de un fichero txt")
        print (str(IndexError))