#!/usr/bin/env python3
#coding=utf-8

import glob
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF

procesador_pdf=ProcesadorPDF()
pdfs=glob.glob("*.pdf")
for pdf in pdfs:
    procesador_pdf.convertir_a_txt(pdf)
    
    
ficheros_eemm=glob.glob("*05*.txt")
print (ficheros_eemm)