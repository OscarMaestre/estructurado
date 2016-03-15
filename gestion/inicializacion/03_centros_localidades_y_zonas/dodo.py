#!/usr/bin/env python3
#coding=utf-8

import glob
from utilidades.ficheros.ProcesadorPDF  import ProcesadorPDF
from utilidades.ficheros.GestorFicheros import GestorFicheros

ficheros_pdf = ["LocalidadesColegiosCGTConvocadoNov2015.pdf",
                "LocalidadesIESCGTConvocadoNov2015.pdf",
                "LocalidadesEACGTConvocadoNov2015.pdf",
                "LocalidadesEOICGTConvocadoNov2015.pdf",
                 "LocalidadesCPMCGTConvocadoNov2015.pdf",
                 "LocalidadesCEPASCGTConvocadoNov2015.pdf"]

procesador_pdf = ProcesadorPDF()
gf=GestorFicheros()

nombre_fichero_coles_txt    =   procesador_pdf.convertir_a_txt ( ficheros_pdf[0] )
nombre_fichero_ies_txt      =   procesador_pdf.convertir_a_txt ( ficheros_pdf[1] )
nombre_fichero_ea_txt       =   procesador_pdf.convertir_a_txt ( ficheros_pdf[2] )
nombre_fichero_eoi_txt      =   procesador_pdf.convertir_a_txt ( ficheros_pdf[3] )
nombre_fichero_cpm_txt      =   procesador_pdf.convertir_a_txt ( ficheros_pdf[4] )
nombre_fichero_cepas_txt    =   procesador_pdf.convertir_a_txt ( ficheros_pdf[5] )

    
gf.ejecutar_comando ( "./procesar_colegios.py", nombre_fichero_coles_txt)
gf.ejecutar_comando ( "./procesar_ea.py", nombre_fichero_ea_txt)
gf.ejecutar_comando ( "./procesar_eoi.py", nombre_fichero_eoi_txt)
gf.ejecutar_comando ( "./procesar_ea.py", nombre_fichero_cpm_txt)
gf.ejecutar_comando ( "./procesar_cepas.py", nombre_fichero_cepas_txt)
gf.ejecutar_comando ( "./procesar_ies.py", nombre_fichero_ies_txt)