#!/usr/bin/env python3
#coding=utf-8

import sys, os, re, csv
from utilidades.basedatos.Configurador import Configurador
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import django
from django.db import transaction
NUM_DIRECTORIO_ANTERIORES=2
DIRECTORIOS_ANTERIORES=[".."] * NUM_DIRECTORIO_ANTERIORES

configurador=Configurador (os.path.sep.join (DIRECTORIOS_ANTERIORES) )

configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

ARCHIVO=sys.argv[1]
ARCHIVO_RESULTADO=ARCHIVO[:-4]+".csv"

procesador_pdf=ProcesadorPDF()
lineas_fichero=procesador_pdf.abrir_fichero_txt(ARCHIVO)

re_cuerpo="CUERPO"
expr_regular_cuerpo=re.compile ( re_cuerpo )

re_total = "TOTAL "
expr_regular_total = re.compile ( re_total )

re_decimal="[0-9]{3},[0-9]{4}"
expr_regular_decimal=re.compile(re_decimal)

DENEGADO        ="DENEGADO"
PEND_DESTINO    ="PEND. DESTINO"

def extraer_puntuaciones (linea):
    puntos=expr_regular_decimal.findall(linea)
    return puntos
    
def extraer_nombre_persona ( linea ):
    return linea[0:38].strip()

def extraer_cuerpo ( linea ):
    (ini, fin, palabra_cuerpo) = procesador_pdf.linea_contiene_patron (
        expr_regular_cuerpo, linea )
    return linea[fin+2:fin+8].strip()

def extraer_puntuacion_total ( linea ):
    (ini, fin, palabra_cuerpo) = procesador_pdf.linea_contiene_patron (
        expr_regular_total, linea )
    return linea[fin:fin+10]

def extraer_codigo_centro ( linea ):
    (ini, fin, cod_centro) = procesador_pdf.linea_contiene_patron (
        procesador_pdf.expr_regular_codigo_centro_sin_c, linea )
    return cod_centro

fichero_resultado=open ( ARCHIVO_RESULTADO, "w", newline="")
fichero_csv = csv.writer ( fichero_resultado, delimiter=",",
                          quotechar="\"")
while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual().strip()
    (ini, fin, dni)=procesador_pdf.linea_actual_contiene_patron ( procesador_pdf.expr_regular_dni )
    if dni!=procesador_pdf.PATRON_NO_ENCONTRADO:
        
        nombre_persona  = extraer_nombre_persona ( linea )
        cuerpo          = extraer_cuerpo ( linea )

        #La puntuacion total esta en la siguiente linea, hay que avanzar
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        punt_total      = extraer_puntuacion_total ( linea )
        punt_total      = punt_total.strip()
        
        #Los subapartados estan en la siguiente linea
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        punt_subapartados=extraer_puntuaciones ( linea )
        
        #El destino anterior esta en la siguiente linea
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        cod_centro_anterior =extraer_codigo_centro ( linea )
        especialidad_anterior=linea[-4:].strip()
        
        #El destino siguiente está dos lineas mas adelante
        procesador_pdf.siguiente_linea()
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        cod_centro_def =extraer_codigo_centro ( linea )
        especialidad_def=linea[-4:].strip()
        fichero_csv.writerow  ( [dni, nombre_persona, cuerpo, punt_total,
               cod_centro_anterior, especialidad_anterior,
               cod_centro_def, cuerpo+especialidad_def] )
        continue
    procesador_pdf.siguiente_linea()
#print (ARCHIVO_RESULTADO)