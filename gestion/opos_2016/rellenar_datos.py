#!/usr/bin/env python3
# coding=utf-8



from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
from django.db import transaction


def crear_localidad(cod_localidad, nom_localidad, provincia_asociada):
    try:
        loc=LocalidadOpos2016(codigo_localidad=cod_localidad,
                              nombre_localidad=nom_localidad,
                              provincia=provincia_asociada)
        loc.save()
        return loc
    except:
        loc=LocalidadOpos2016.objects.get(codigo_localidad=cod_localidad)
        return loc

def crear_centro(cod_centro, nom_centro, localidad_asociada):
    try:
        centro=CentroOpos2016(codigo_centro=cod_centro,
                              nombre_centro=nom_centro,
                              localidad=localidad_asociada)
        centro.save()
    except:
        return 

def get_fila(nombre_loc, gestor_bd):
    sql="select origen, destino, minutos, distancia from rutas where origen='{0}'".format(nombre_loc)  
    #print (sql)
    filas=gestor_bd.get_filas ( sql )
    if len(filas)!=0:
        resultado=filas[0]
        return resultado
    sql="select origen, destino, minutos, distancia from rutas where destino='{0}'".format(nombre_loc)  
    #print (sql)
    filas=gestor_bd.get_filas ( sql )
    if len(filas)!=0:
        resultado=filas[0]
        return resultado
    print (nombre_loc+" no encontrada")

RutaOpos2016.objects.all().delete()
LocalidadOpos2016.objects.all().delete()
ProvinciaOpos2016.objects.all().delete()
CentroOpos2016.objects.all().delete()


prov_ab=ProvinciaOpos2016("800010", "Albacete")
prov_cr=ProvinciaOpos2016("800299", "Ciudad Real")
prov_cu=ProvinciaOpos2016("800388", "Cuenca")
prov_gu=ProvinciaOpos2016("800477", "Guadalajara")
prov_to=ProvinciaOpos2016("800566", "Toledo")
gestor_bd=GestorBD("rutas.db")

objetos_provincia={
    prov_ab.codigo_provincia:prov_ab,
    prov_cr.codigo_provincia:prov_cr,
    prov_cu.codigo_provincia:prov_cu,
    prov_gu.codigo_provincia:prov_gu,
    prov_to.codigo_provincia:prov_to
}

fichero=sys.argv[1]

descriptor=open(fichero)
lineas = descriptor.readlines()
descriptor.close()


with transaction.atomic():
    for l in lineas:
        trozos=l.strip().split(":")
        cod_provincia   =   trozos[0]
        nom_provincia   =   trozos[1]
        cod_localidad   =   trozos[2]
        nom_localidad   =   trozos[3]
        cod_centro      =   trozos[4]
        nom_centro      =   trozos[5]
        #Los nombres de localidad suelen tener errores como
        #llevar el articulo delante
        nom_localidad=rectificar_nombre_localidad(nom_localidad)
        
        provincia_asociada=objetos_provincia[cod_provincia]
        localidad=crear_localidad(cod_localidad, nom_localidad, provincia_asociada)
        f=get_fila ( nom_localidad, gestor_bd )
        centro=crear_centro ( cod_centro, nom_centro, localidad)
        