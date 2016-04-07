#!/usr/bin/env python3
# coding=utf-8
import re

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
procesador_pdf=ProcesadorPDF()
ULTIMA_RELACION_INTERINOS="Ultima0597.pdf"
nombre_txt=procesador_pdf.convertir_a_txt(ULTIMA_RELACION_INTERINOS)

procesador_pdf.abrir_fichero_txt(nombre_txt)


re_especialidad="Especialidad\s+[0-9]{3}"
expr_regular_especialidad=re.compile ( re_especialidad )
codigo_especialidad_actual=""
lista_ultimos_datos_interinos=[]
numero_de_orden=1
while not procesador_pdf.FIN_DE_FICHERO:
    linea=procesador_pdf.get_linea_actual()
    (ini, fin, especialidad)=procesador_pdf.linea_actual_contiene_patron(expr_regular_especialidad)
    if especialidad!=procesador_pdf.PATRON_NO_ENCONTRADO:
        codigo_especialidad_actual="0597" + especialidad[-3:]
        numero_de_orden=1
        print ("Especialidad actual:"+codigo_especialidad_actual)
    (ini_dni, fin_dni, dni)=procesador_pdf.avanzar_buscando_dni(debe_estar_en_misma_linea=True)
    if dni!=procesador_pdf.PATRON_NO_ENCONTRADO:
        #print (dni)
        nombre_completo=linea[fin_dni:68].strip()
        print (dni, nombre_completo)
        
    procesador_pdf.siguiente_linea()
