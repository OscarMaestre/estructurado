#!/usr/bin/env python3
#coding=utf-8

import sys, os, re
from utilidades.basedatos.Configurador import Configurador
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join ([".."]) )

configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *

re_nombre_completo="  [A-ZÁÉÍÓÚÜÑ ]+, [A-ZÁÉÍÓÚÜÑ ]+"
expr_regular_nombre = re.compile ( re_nombre_completo )



def con_ingles(linea):
    if linea[91:121].find("S")!=-1:
        return True
    return False

def con_frances(linea):
    if len(linea)<121:
        return False
    if linea[122:].find("S")!=-1:
        return True
    return False

bolsas=[]
for tupla in InterinoDisponible.POSIBLES_BOLSAS:
    bolsas.append("("+tupla[0]+")")
re_posible_bolsa="|".join(bolsas)
re_posible_bolsa="("+ re_posible_bolsa +")"
re_posible_bolsa += "\s+[0-9]{1,4} "
expr_regular_bolsa=re.compile( re_posible_bolsa )
print (re_posible_bolsa)

procesador_pdf=ProcesadorPDF()
fich_txt=procesador_pdf.convertir_a_txt ( sys.argv[1] )
print ("Procesando {0}".format (fich_txt) )

procesador_pdf.abrir_fichero_txt ( fich_txt )

while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual().strip()
    (ini_dni, fin_dni, dni)=procesador_pdf.linea_contiene_patron(
        procesador_pdf.expr_regular_dni, linea)
    if dni!=procesador_pdf.PATRON_NO_ENCONTRADO:
        num_orden=linea[:4].strip()
        (ini_bolsa, fin_bolsa, bolsa)=procesador_pdf.linea_contiene_patron(
            expr_regular_bolsa, linea)
        nombre_completo=linea[fin_dni+1:ini_bolsa-1].strip()
        habla_ingles=con_ingles(linea)
        habla_frances=con_ingles(linea)
        print (dni, nombre_completo, bolsa, habla_ingles, habla_frances)
        if bolsa==procesador_pdf.PATRON_NO_ENCONTRADO:
            print ("Error, bolsa no encontrada en esta linea")
            print (linea)
    procesador_pdf.siguiente_linea()
    
print (procesador_pdf.expr_regular_dni)

