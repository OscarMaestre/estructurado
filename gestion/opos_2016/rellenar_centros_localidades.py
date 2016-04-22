#!/usr/bin/env python3
# coding=utf-8



from utilidades.basedatos.Configurador import Configurador

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
    except Exception as e:
        print (e)
        loc=LocalidadOpos2016.objects.get(codigo_localidad=cod_localidad)
        return loc

def crear_centro(cod_centro, nom_centro, localidad_asociada):
    try:
        centro=CentroOpos2016(codigo_centro=cod_centro,
                              nombre_centro=nom_centro,
                              localidad=localidad_asociada)
        centro.save()
    except Exception as e:
        print (nom_centro+" no creado")
        print (e)
        return 


LocalidadOpos2016.objects.all().delete()
ProvinciaOpos2016.objects.all().delete()
CentroOpos2016.objects.all().delete()


prov_ab=ProvinciaOpos2016("800010", "Albacete")
prov_cr=ProvinciaOpos2016("800299", "Ciudad Real")
prov_cu=ProvinciaOpos2016("800388", "Cuenca")
prov_gu=ProvinciaOpos2016("800477", "Guadalajara")
prov_to=ProvinciaOpos2016("800566", "Toledo")

prov_ab.save()
prov_cr.save()
prov_cu.save()
prov_to.save()
prov_gu.save()

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
        centro=crear_centro ( cod_centro, nom_centro, localidad)
