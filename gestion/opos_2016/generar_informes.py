#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
from utilidades.ficheros.GestorFicheros import GestorFicheros

import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
from django.db import transaction
from django.template.loader import render_to_string, get_template


RUTA_INFORMES="./informes"

prov_cr=ProvinciaOpos2016.objects.filter(nombre_provincia="Ciudad Real")
#print (prov_cr)
localidades=LocalidadOpos2016.objects.filter(provincia=prov_cr)
#print (localidades)



def convertir_minutos_a_cad(minutos):
    return minutos

def generar_informe(localidad):
    
    rutas=RutaOpos2016.objects.filter(origen=localidad).order_by("minutos")
    
    cad=""
    for r in rutas:
        tiempo_aprox=convertir_minutos_a_cad ( r.minutos )
        cad+="""
        * Código {0}, localidad:{1},  tiempo aprox {2}, distancia aprox {3}\r\n
        """.format (
            r.destino.codigo_localidad,
            r.destino.nombre_localidad,
            tiempo_aprox, r.distancia)
        centros_asociados=r.destino.centroopos2016_set.all()
        #print ("\t", r)
        for c in centros_asociados:
            cad+="""
            \r\n\t** Codigo:{0}, centro:{1}
            """.format (c.codigo_centro, c.nombre_centro)
        #print (dir(centros_asociados))
    contexto={
        "listado":cad
    }
    informe=render_to_string("index/informe.rest", contexto)
    return informe
    
        
        
gf=GestorFicheros()
for l in localidades:
    archivo_rst=RUTA_INFORMES + os.sep + l.nombre_localidad+".rst"
    archivo_tex=RUTA_INFORMES + os.sep + l.nombre_localidad+".tex"
    print (archivo_rst, archivo_tex)
    informe=generar_informe ( l )
    descriptor=open(archivo_rst, "w")
    descriptor.write(informe)
    descriptor.close()
    gf.ejecutar_comando ("rst2latex", archivo_rst, archivo_tex)
    
