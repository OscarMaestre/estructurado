#!/usr/bin/env python3
#coding=utf-8


from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import sys
procesador_pdf=ProcesadorPDF()

fich_txt=procesador_pdf.convertir_a_txt ( sys.argv[1] )
procesador_pdf.abrir_fichero_txt ( fich_txt )

LOCALIDAD="Localidad:"
CODIGO="Código:"

def get_localidad(linea):
    pos_inicio_localidad=linea.find(LOCALIDAD)
    
leyendo_centros=False
while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual()
    if linea.find(LOCALIDAD)!=-1:
        #Averiguamos el nombre de la localidad
        pos_inicio_localidad=linea.find(LOCALIDAD)
        pos_inicio_codigo=linea.find(CODIGO)
        pos_fin_localidad=pos_inicio_localidad + len(LOCALIDAD)
        #Esta es la localidad
        nom_localidad=linea[pos_fin_localidad:pos_inicio_codigo].strip()
        #Y este el codigo de la localidad
        cod_localidad=""
        pos_fin_codigo=pos_inicio_codigo+len(CODIGO)
        cod_localidad=linea[pos_fin_codigo:].strip()
        print (cod_localidad, nom_localidad)
    
    #Si nos encontramos la palabra "Centro" hay que empezar a leer centros
    if linea.find("Centro"):
        leyendo_centros=True
        #Y pasamos a la siguiente linea
        procesador_pdf.siguiente_linea()
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        while linea!="":
            nombre_centro=linea[:88].strip()
            codigo_centro=linea[89:].strip()
            print("\t{0}, {1}".format(codigo_centro, nombre_centro))
            procesador_pdf.siguiente_linea()
            linea=procesador_pdf.get_linea_actual().strip()
        
    procesador_pdf.siguiente_linea()