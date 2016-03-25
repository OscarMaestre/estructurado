#!/usr/bin/env python3
#coding=utf-8

from bs4 import BeautifulSoup #sudo pip3 install BeautifulSoup4

from utilidades.ficheros.GestorFicheros import GestorFicheros
from utilidades.basedatos.Configurador import Configurador
from constantes import *

import os
import django
from django.db import transaction


configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

gf=GestorFicheros()

def extraer_cadena_div(div_padre, etiqueta, clase_css):
    elemento_extraido=div_padre.find(etiqueta, clase_css)
    if elemento_extraido==None:
        return ""
    cad=elemento_extraido.string.strip()
    return cad

def procesar_archivo_centro(nombre_archivo):
    lista_ensenanzas=[]
    descriptor_fichero= open ( nombre_archivo, "r" )
    sopa = BeautifulSoup ( descriptor_fichero, "html.parser")
    div_tabla_ensenanzas=sopa.find_all("tr", "valueDetail")
    for div in div_tabla_ensenanzas:
        nombre_ensenanzas   = extraer_cadena_div ( div, "td", "valueDetailViewENSEÑANZA")
        regimen             = extraer_cadena_div ( div, "td", "valueDetailViewREGIMEN")
        unidades            = extraer_cadena_div ( div, "td", "valueDetailViewNUMUND_ENS")
        puestos             = extraer_cadena_div ( div, "td", "valueDetailViewNUMPTO_ENS")
        uds_concertadas     = extraer_cadena_div ( div, "td", "valueDetailViewNUMUNDCON")
        fecha_acceso        = extraer_cadena_div ( div, "td", "valueDetailViewFECHRENCON")
        if nombre_ensenanzas=="":
            continue
        e=Ensenanza( nombre_ensenanzas, regimen, unidades, puestos, uds_concertadas, fecha_acceso)
        #print( nombre_ensenanzas, regimen, unidades, puestos, uds_concertadas, fecha_acceso)
        lista_ensenanzas.append(e)
    return lista_ensenanzas
    

    

lista_centros=[]


for i in range ( 0, TOTAL_PAGINAS):
#for i in range ( 0, 50):
    nombre_fichero = FICHERO_BASE.format ( i )
    descriptor_fichero= open ( nombre_fichero, "r" )
    sopa = BeautifulSoup ( descriptor_fichero, "html.parser")
    #print ( sopa.prettify() )
    div_centros =sopa.find_all  ( "div", "elementList" )
    for centro in div_centros:
        #Naturaleza
        div_natu = centro.find ("div", "campListNATURALEZA")
        natu = div_natu.string.strip()
        
        #Enlace a mas informacion
        enlace_nombre= centro.find ("div", "campListNOMBRE")
        enlace_centro = enlace_nombre.a["href"]
        nom_centro=enlace_nombre.a.string.strip()
        
        #Codigo del centro
        div_cod_centro= centro.find ("div", "campListCENTID")
        cod_centro=div_cod_centro.string.strip()
        cod_centro=cod_centro.replace("[", "")
        cod_centro=cod_centro.replace("]", "")
        #Se descarga el fichero ampliado
        url_informacion_centro = URL_JUNTA + enlace_centro
        fichero_mas_informacion=NOMBRE_FICHERO_INFORMACION_CENTRO.format (cod_centro)
        if not gf.existe_fichero ( fichero_mas_informacion ):
            gf.descargar_fichero (url_informacion_centro, fichero_mas_informacion)
        
        div_dir_postal=centro.find("div", "campListDOMICILIO")
        dir_postal=div_dir_postal.string.strip()
        
        
        div_cod_postal=centro.find("div", "campListCP")
        cod_postal=div_cod_postal.string.strip()[4:]
        
        div_localidad=centro.find("div", "campListLOCALIDAD")
        nombre_localidad=div_localidad.string.strip()
        nom_localidad=rectificar_nombre_localidad(nombre_localidad)
        try:
            localidad_asociada=Localidad.objects.get(nombre_localidad=nom_localidad)
            
        except :
            print ("Ops, no existe la localidad:"+nom_localidad)
            continue 
            
        div_provincia=centro.find("div", "campListPROVINCIA")
        nombre_provincia=div_provincia.string.strip()
        nombre_provincia=nombre_provincia.replace("(", "")
        nombre_provincia=nombre_provincia.replace(")", "")
        
        
        div_telefono=centro.find("div", "campListTELEFONO")
        if div_telefono==None:
            telefono=""
        else:
            telefono=div_telefono.string.strip()
        
        
        div_fax=centro.find("div", "campListFAX")
        if div_fax==None:
            numero_fax=""
        else:
            numero_fax=div_fax.string.strip()
        
        
        div_email=centro.find("div", "campListEMAIL")
        if div_email==None:
            correo_electronico=""
        else:
            correo_electronico=div_email.a.string.strip()
        
        
        div_web=centro.find("div", "campListWEB")
        if div_web==None:
            pag_web=""
        else:
            pag_web=div_web.a.string.strip()
        
        
        #lista_ensenanzas=[]
        #if gf.existe_fichero ( fichero_mas_informacion ):
        #    lista_ensenanzas=procesar_archivo_centro ( fichero_mas_informacion )
        
        c=Centro
        
        lista_centros.append ( (natu, cod_centro, nom_centro,
                 dir_postal,cod_postal,
                 localidad_asociada, telefono, numero_fax,
                 correo_electronico, pag_web) )
        
with transaction.atomic():
    for tupla in lista_centros:
        try:
            centro_asociado=Centro.objects.get(codigo_centro=tupla[1]+"C")
        except :
            
            centro_asociado=Centro(codigo_centro=tupla[1]+"C",
                                   nombre_centro=tupla[2],
                                   localidad=tupla[5],
                                   naturaleza=tupla[0]
                                   )
            centro_asociado.save()
            print ("El centro {0}, {1}, {2} no existía".format ( tupla[1]+"C", tupla[2], tupla[0]) )
        direccion_centro=DireccionesCentro (
            centro=centro_asociado,
            direccion_postal=tupla[3],
            codigo_postal=tupla[4],
            localidad=localidad_asociada,
            tlf=tupla[6], fax=tupla[7],
            email=tupla[8], web=tupla[8]
        )
        direccion_centro.save()