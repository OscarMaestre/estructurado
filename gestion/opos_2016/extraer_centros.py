#!/usr/bin/env python3
#coding=utf-8


from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import sys
procesador_pdf=ProcesadorPDF()

fich_txt=procesador_pdf.convertir_a_txt ( sys.argv[1] )
procesador_pdf.abrir_fichero_txt ( fich_txt )

while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual()
    print ( linea )
    procesador_pdf.siguiente_linea()