#!/usr/bin/env python3
#coding=utf-8

from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
from utilidades.ficheros.GestorFicheros import GestorFicheros

import sys, os

configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
from django.db import transaction
from django.template.loader import render_to_string, get_template


RUTA_INFORMES="./informes"

#Borramos Herrera y todos los centros penitenciarios
herrera=LocalidadOpos2016.objects.filter(nombre_localidad__contains="Herrera").all()
herrera.delete()

centros_penitenciarios=CentroOpos2016.objects.filter(
    nombre_centro__contains="Penitenciari").all()
print (centros_penitenciarios)
centros_penitenciarios=CentroOpos2016.objects.filter(
    nombre_centro__contains="Penitenciari").all()
centros_penitenciarios.delete()


prov_cr=ProvinciaOpos2016.objects.filter(nombre_provincia="Ciudad Real")
#print (prov_cr)
localidades=LocalidadOpos2016.objects.filter(provincia=prov_cr)
#print (localidades)

item_pueblo="""
- ``{0}`` {1}  ({2}, {3} km)
"""
item_centro="""
  -``{0}`` {1}
    
"""
def convertir_minutos_a_cad(minutos):
    numero_minutos=int(minutos)
    horas=numero_minutos//60
    if horas==0:
        return str(minutos) +" minutos"
    resto_minutos=minutos-(60*horas)
    if resto_minutos==0:
        return "{0}h".format ( horas )
    return "{0}h {1}min".format ( horas, resto_minutos )

def generar_informe(localidad):
    
    rutas=RutaOpos2016.objects.filter(origen=localidad).order_by("minutos")
    nombre_localidad=localidad.nombre_localidad
    cad=""
    for r in rutas:
        tiempo_aprox=convertir_minutos_a_cad ( r.minutos )
        cad+=item_pueblo.format (
            r.destino.codigo_localidad,
            r.destino.nombre_localidad,
            tiempo_aprox, r.distancia)
        centros_asociados=r.destino.centroopos2016_set.all()
        #print ("\t", r)
        for c in centros_asociados:
            cad+=item_centro.format (c.codigo_centro, c.nombre_centro)
        #print (dir(centros_asociados))
    contexto={
        "listado":cad,
        "localidad":nombre_localidad
    }
    informe=render_to_string("index/informe.rest", contexto)
    return informe
    
        
        
gf=GestorFicheros()
for l in localidades:
    nombre_para_archivos=l.nombre_localidad.replace(" ", "_")
    archivo_rst=RUTA_INFORMES + os.sep + nombre_para_archivos +".rst"
    archivo_tex=RUTA_INFORMES + os.sep + nombre_para_archivos +".tex"
    print (archivo_rst, archivo_tex)
    informe=generar_informe ( l )
    descriptor=open(archivo_rst, "w")
    descriptor.write(informe)
    descriptor.close()
    gf.ejecutar_comando ("rst2latex", archivo_rst, archivo_tex)
    os.chdir(RUTA_INFORMES)
    gf.ejecutar_comando ("pdflatex", nombre_para_archivos+".tex")
    gf.ejecutar_comando ("pdflatex", nombre_para_archivos +".tex")
    gf.ejecutar_comando ("rm", nombre_para_archivos +".out")
    gf.ejecutar_comando ("rm", nombre_para_archivos +".tex")
    gf.ejecutar_comando ("rm", nombre_para_archivos +".log")
    gf.ejecutar_comando ("rm", nombre_para_archivos +".aux")
    os.chdir("..")
    
os.chdir ( RUTA_INFORMES )

    
