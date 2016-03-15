#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.basedatos.Configurador import Configurador
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

zona_clm=Zona.get_zona_clm()
print (zona_clm)

nombres_provincia=["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"]

def extraer_provincia(procesador_pdf, codigo_anterior):
    linea_actual=procesador_pdf.get_linea_actual()
    pos=linea_actual.find("Provincia")
    if linea_actual.find("Provincia")!=-1:
       codigo_provincia_actual=Provincia.get_codigo(linea_actual[14:].strip())
       print ("Examinando IES en provincia "+codigo_provincia_actual)
       return codigo_provincia_actual
    return codigo_anterior

def crear_entidades ( procesador_pdf ):
    cepas=[]
    localidades=[]
    codigo_provincia_actual=""
    while not procesador_pdf.eof():
        codigo_provincia_actual=extraer_provincia(procesador_pdf, codigo_provincia_actual)
        (ini_cod_centro, fin_cod_centro, cod_centro)=procesador_pdf.avanzar_buscando_codigo_centro(
            debe_estar_en_misma_linea=True, con_c=True
        )
        if (cod_centro!=procesador_pdf.PATRON_NO_ENCONTRADO):
            (ini_cod_localidad, fin_cod_localidad, cod_localidad)=procesador_pdf.avanzar_buscando_codigo_localidad(
                debe_estar_en_misma_linea=True
            )
            linea_actual=procesador_pdf.get_linea_actual()
            nombre_centro=linea_actual[11:ini_cod_localidad-1]
            nombre_localidad=linea_actual[fin_cod_localidad+1:].strip()
            nombre_centro=nombre_centro.strip()
            
            cepas.append ( (cod_centro, nombre_centro, cod_localidad) )
            localidades.append ( (cod_localidad, nombre_localidad, codigo_provincia_actual) )
            print ("-{0}- -{1}- -{2}- -{3}- -{4}-".format(
                cod_centro, nombre_centro, cod_localidad, nombre_localidad, codigo_provincia_actual))
        procesador_pdf.siguiente_linea()
    #Fin del while
    with transaction.atomic():
        for l in localidades:
            prov_asociada=Provincia.objects.get ( provincia = l[2])
            l=Localidad( codigo_localidad = l[0], nombre_localidad=l[1],
                        provincia=prov_asociada, zona=zona_clm)
            l.save()
    with transaction.atomic():
        for c in cepas:
            localidad_asociada=Localidad.objects.get( codigo_localidad=c[2])
            cepa=Centro(codigo_centro=c[0], nombre_centro=c[1], localidad=localidad_asociada)
            cepa.save()
            
if __name__ == '__main__':
    procesador_pdf=ProcesadorPDF()
    try:
        procesador_pdf.abrir_fichero_txt ( sys.argv[1] )
        crear_entidades(procesador_pdf)
    except IndexError:
        print ("Indique el nombre de un fichero txt")