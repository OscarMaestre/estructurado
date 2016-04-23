#!/usr/bin/env python3
#coding=utf-8

import sys, re
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.ficheros.GestorFicheros import GestorFicheros
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



def get_codigo_localidad(procesador_pdf):
    (ini_cod_localidad, fin_cod_localidad, cod_localidad)=procesador_pdf.linea_actual_contiene_codigo_localidad()
    while cod_localidad==procesador_pdf.PATRON_NO_ENCONTRADO:
        procesador_pdf.siguiente_linea()
        linea_actual=procesador_pdf.get_linea_actual()
        (ini_cod_localidad, fin_cod_localidad, cod_localidad)=procesador_pdf.linea_actual_contiene_codigo_localidad()
    return (ini_cod_localidad, fin_cod_localidad, cod_localidad)


def get_tipo_centro(nombre_centro):
    if nombre_centro.find("IESO")!=-1:
        return "IESO"
    if nombre_centro.find("IES")!=-1:
        return "IES"
    if nombre_centro.find("SES")!=-1:
        return "SES"
    return "CIFP"
procesador_pdf=ProcesadorPDF()
procesador_pdf.abrir_fichero_txt ( sys.argv[1] )

institutos=[]
while not procesador_pdf.eof():
    (ini_cod_centro, fin_cod_centro,
        cod_centro)=procesador_pdf.linea_actual_contiene_codigo_centro (con_c=True)
    if cod_centro!=procesador_pdf.PATRON_NO_ENCONTRADO:
        (ini_cod_localidad, fin_cod_localidad, cod_localidad)=get_codigo_localidad ( procesador_pdf )
        linea_actual=procesador_pdf.get_linea_actual()
        nombre_centro=linea_actual[fin_cod_centro+1:ini_cod_localidad-1].strip()
        
        #Este instituto casi siempre está mal colocado debido a lo largo que es
        if cod_centro=="13000566C":
            nombre_centro="IES San Juan Bautista de la Concepcion"
        tipo_centro=get_tipo_centro ( nombre_centro )
        print (cod_centro, nombre_centro, cod_localidad, ">"+tipo_centro+"<")
        institutos.append ( (cod_centro, nombre_centro, cod_localidad, tipo_centro ) )
    procesador_pdf.siguiente_linea()
    
with transaction.atomic():
    for ies in institutos:
        localidad_asociada=Localidad.objects.get( codigo_localidad = ies[2])
        objeto_centro=Centro (
            codigo_centro = ies[0],nombre_centro=ies[1], localidad=localidad_asociada,
            tipo_centro=ies[3]
        )
        objeto_centro.save()
  


#La academia de Infanteria de Toledo no aparece en listados, pero existe
#y es asignable

toledo=Localidad.objects.get( codigo_localidad = "451680001")
academia_infanteria=Centro( codigo_centro = "45600235C",
                           nombre_centro="Academia de Infanteria de Toledo",
                           localidad=toledo, tipo_centro="IES")
academia_infanteria.save()
                             
                             
#La UO del CEIP Francisco Giner de los Rios aun parece existir
villarrobledo=Localidad.objects.get( codigo_localidad = "020810003")
uo_giner_rios=Centro( codigo_centro = "02008439C",
                           nombre_centro="UO CP Francisco Giner de los Rios",
                           localidad=villarrobledo, tipo_centro="IES")
uo_giner_rios.save()


#La DP de ciudad real
ciudad_real=Localidad.objects.get( codigo_localidad = "130340002")
dp_ciudad_real=Centro( codigo_centro = "13003683C",
                           nombre_centro="Deleg Prov Educación Ciudad Real",
                           localidad=ciudad_real, tipo_centro="DP")
dp_ciudad_real.save()

#Localidades "vacías"
paro_interinos=Centro(codigo_centro="9999C", nombre_centro="En paro maestros",
                      localidad=ciudad_real, tipo_centro="CEIP")
paro_interinos.save()
paro_eemm=Centro(codigo_centro="9998C", nombre_centro="En paro EEMM",
                      localidad=ciudad_real, tipo_centro="IES")
paro_eemm.save()

jubilados=Centro(codigo_centro="90C", nombre_centro="Jubilados",
                      localidad=ciudad_real, tipo_centro="IES")
jubilados.save()

fuera_prov=Centro(codigo_centro="9559C", nombre_centro="Def. fuera provincia",
                      localidad=ciudad_real, tipo_centro="IES")
fuera_prov.save()

int_fuera_prov=Centro(codigo_centro="9555C", nombre_centro="Int. fuera provincia",
                      localidad=ciudad_real, tipo_centro="IES")
int_fuera_prov.save()

desconocido=Centro(codigo_centro="9000C", nombre_centro="Desconocido",
                      localidad=ciudad_real, tipo_centro="IES")
desconocido.save()


uo_ciudad_jardin=Centro( codigo_centro = "13010274C",
                           nombre_centro="UO Ciudad Jardin",
                           localidad=ciudad_real, tipo_centro="UO")
uo_ciudad_jardin.save()
#puertollano=Localidad.objects.get( codigo_localidad = "1307100004")
#virgen_de_gracia=Centro( codigo_centro = "13003683C",
#                           nombre_centro="Ifp Virgen de Gracia",
#                           localidad=puertollano)
#virgen_de_gracia.save()


#UO CEE Ciudad de toledo
toledo=Localidad.objects.get( codigo_localidad = "451680001")
uo_cee_toledo=Centro( codigo_centro = "45011707C",
                           nombre_centro="UO CEE Ciudad de Toledo",
                           localidad=ciudad_real, tipo_centro="UO")
uo_cee_toledo.save()
