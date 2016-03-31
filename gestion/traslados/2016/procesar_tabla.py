#!/usr/bin/env python3
#coding=utf-8

import sys, os
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
procesador_pdf=ProcesadorPDF()
lineas_fichero=procesador_pdf.abrir_fichero_txt(ARCHIVO)

while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual().strip()
    (ini, fin, patron)=procesador_pdf.linea_actual_contiene_patron ( procesador_pdf.expr_regular_dni )
    if patron!=procesador_pdf.PATRON_NO_ENCONTRADO:
        print (patron)
    procesador_pdf.siguiente_linea()