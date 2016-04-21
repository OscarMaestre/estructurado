#!/usr/bin/env python3
#coding=utf-8


from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import sys
procesador_pdf=ProcesadorPDF()

fich_txt=procesador_pdf.convertir_a_txt ( sys.argv[1] )
procesador_pdf.abrir_fichero_txt ( fich_txt )

LOCALIDAD="Localidad:"
CODIGO="Código:"
PROVINCIA="Provincia:"


leyendo_centros=False
cod_localidad_actual=""
nom_localidad_actual=""
nom_provincia_actual=""
cod_provincia_actual=""

#Las primeras 20 lineas del fichero contienen cosas que no nos interesan
for i in range(0, 18):
    procesador_pdf.siguiente_linea()
    
while not procesador_pdf.eof():
    linea=procesador_pdf.get_linea_actual().strip()
    if linea.find(PROVINCIA)!=-1:
        pos_inicio_provincia=linea.find(PROVINCIA)+len(PROVINCIA)
        pos_inicio_codigo=linea.find(CODIGO)
        nom_provincia_actual=linea[pos_inicio_provincia:pos_inicio_codigo-1].strip()
        pos_fin_codigo=pos_inicio_codigo+len(CODIGO)
        cod_provincia_actual=linea[pos_fin_codigo:].strip()
        
    if linea.find(LOCALIDAD)!=-1:
        #Averiguamos el nombre de la localidad
        pos_inicio_localidad=linea.find(LOCALIDAD)+len(LOCALIDAD)
        pos_inicio_codigo=linea.find(CODIGO)
        pos_fin_localidad=pos_inicio_localidad + len(LOCALIDAD)
        #Esta es la localidad
        nom_localidad=linea[pos_fin_localidad:pos_inicio_codigo].strip()
        #Y este el codigo de la localidad
        cod_localidad=""
        pos_fin_codigo=pos_inicio_codigo+len(CODIGO)
        cod_localidad=linea[pos_fin_codigo:].strip()
        cod_localidad_actual=cod_localidad
        nom_localidad_actual=nom_localidad
    
    #Si nos encontramos la palabra "Centro" hay que empezar a leer centros
    if linea.find("Centro")!=-1:
        leyendo_centros=True
        #Y pasamos a la siguiente linea
        #procesador_pdf.siguiente_linea()
        procesador_pdf.siguiente_linea()
        linea=procesador_pdf.get_linea_actual().strip()
        while linea!="":
            nombre_centro=linea[:88].strip()
            codigo_centro=linea[89:].strip()
            registro=":".join([cod_provincia_actual, nom_provincia_actual,cod_localidad_actual, nom_localidad_actual, codigo_centro, nombre_centro])
            print(registro)
            procesador_pdf.siguiente_linea()
            linea=procesador_pdf.get_linea_actual().strip()
        
    procesador_pdf.siguiente_linea()