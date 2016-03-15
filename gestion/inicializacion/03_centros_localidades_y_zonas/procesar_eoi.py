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
def crear_entidades ( procesador_pdf ):
    escuelas_adultos=[]
    localidades=[]
    while not procesador_pdf.eof():
        linea_actual=procesador_pdf.get_linea_actual()
        (ini_cod_centro, fin_cod_centro, cod_centro)=procesador_pdf.avanzar_buscando_codigo_centro(
            debe_estar_en_misma_linea=False, con_c=True
        )
        if (cod_centro!=procesador_pdf.PATRON_NO_ENCONTRADO):
            (ini_cod_localidad, fin_cod_localidad, cod_localidad)=procesador_pdf.avanzar_buscando_codigo_localidad(
                debe_estar_en_misma_linea=True
            )
            linea_actual=procesador_pdf.get_linea_actual()
            nombre_centro=linea_actual[33:fin_cod_localidad]
            nombre_localidad=linea_actual[fin_cod_localidad+12:].strip()
            nombre_centro=nombre_centro.strip()
            nombre_provincia=linea_actual[16:30].strip()
            codigo_provincia=Provincia.get_codigo ( nombre_provincia )
            print ("-{0}- -{1}- -{2}- -{3}- -{4}-".format(
                cod_centro, nombre_centro, cod_localidad, nombre_localidad, codigo_provincia))
            escuelas_adultos.append ( (cod_centro, nombre_centro, cod_localidad)   )
            localidades.append ( (cod_localidad, nombre_localidad, codigo_provincia) ) 
        procesador_pdf.siguiente_linea()
    #Fin del while
    
    with transaction.atomic():
        for l in localidades:
            cod_localidad=l[0]
            nom_localidad=l[1]
            codigo_provincia=l[2]
            objeto_provincia_asociada=Provincia.objects.get(provincia=codigo_provincia)
            localidad=Localidad ( codigo_localidad=cod_localidad,
                                 nombre_localidad=nom_localidad,
                                 provincia=objeto_provincia_asociada,
                                 zona=zona_clm)
            localidad.save()
    with transaction.atomic():
        for tupla in escuelas_adultos:
            cod_centro=tupla[0]
            nom_centro=tupla[1]
            cod_localidad=tupla[2]
            localidad_asociada=Localidad.objects.get(codigo_localidad=cod_localidad)
            centro=Centro ( codigo_centro=cod_centro, nombre_centro=nom_centro,
                           localidad=localidad_asociada )
            centro.save()

if __name__ == '__main__':
    procesador_pdf=ProcesadorPDF()
    try:
        procesador_pdf.abrir_fichero_txt ( sys.argv[1] )
        crear_entidades(procesador_pdf)
    except IndexError:
        print ("Indique el nombre de un fichero txt")