#!/usr/bin/env python3

import os, sys, re

NUM_SUBDIRECTORIOS_ANTERIORES=2
SEPARADOR=os.sep

RUTA_PAQUETE_BD=(".."+SEPARADOR) * NUM_SUBDIRECTORIOS_ANTERIORES
DIRECTORIO= RUTA_PAQUETE_BD + os.sep+"Verano"+os.sep+"db_nombramientos"
#aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIRECTORIO)
import GestorDB
import utilidades
import ListaCampos

configuracion_590_fp=[0]*21
configuracion_590_fp[0] ="0590101"
configuracion_590_fp[1] ="0590103"
configuracion_590_fp[2] ="0590102"
configuracion_590_fp[3] ="0590104"
configuracion_590_fp[4] ="0590117"
configuracion_590_fp[5] ="0590105"
configuracion_590_fp[6] ="0590106"
configuracion_590_fp[7] ="0590107"
configuracion_590_fp[8] ="0590108"
configuracion_590_fp[9] ="0590119"
configuracion_590_fp[10]="0590112"
configuracion_590_fp[11]="0590110"
configuracion_590_fp[12]="0590111"
configuracion_590_fp[13]="0590115"
configuracion_590_fp[14]="0590116"
configuracion_590_fp[15]="0590123"
configuracion_590_fp[16]="0590113"
configuracion_590_fp[17]="0590118"
configuracion_590_fp[18]="0590124"
configuracion_590_fp[19]="0590125"
configuracion_590_fp[20]="0590101"

configuracion_590_comunes=[0]*20
configuracion_590_comunes[0] ="0590012"
configuracion_590_comunes[1] ="0590008"
configuracion_590_comunes[2] ="0590803"
configuracion_590_comunes[3] ="0590058"
configuracion_590_comunes[4] ="0590059"
configuracion_590_comunes[5] ="0590009"
configuracion_590_comunes[6] ="0590061"
configuracion_590_comunes[7] ="0590017"
configuracion_590_comunes[8] ="0590001"
configuracion_590_comunes[9] ="0590007"
configuracion_590_comunes[10]="0590010"
configuracion_590_comunes[11]="0590005"
configuracion_590_comunes[12]="0590002"
configuracion_590_comunes[13]="0590011"
configuracion_590_comunes[14]="0590003"
configuracion_590_comunes[15]="0590004"
configuracion_590_comunes[16]="0590006"
configuracion_590_comunes[17]="0590016"
configuracion_590_comunes[18]="0590018"
configuracion_590_comunes[19]="0590019"

configuracion_591_fp=[0]*26
configuracion_591_fp[0] ="0591025"
configuracion_591_fp[1] ="0591026"
configuracion_591_fp[2] ="0591201"
configuracion_591_fp[3] ="0591202"
configuracion_591_fp[4] ="0591214"
configuracion_591_fp[5] ="0591203"
configuracion_591_fp[6] ="0591204"
configuracion_591_fp[7] ="0591206"
configuracion_591_fp[8] ="0591229"
configuracion_591_fp[9] ="0591208"
configuracion_591_fp[10]="0591205"
configuracion_591_fp[11]="0591211"
configuracion_591_fp[12]="0591209"
configuracion_591_fp[13]="0591216"
configuracion_591_fp[14]="0591215"
configuracion_591_fp[15]="0591212"
configuracion_591_fp[16]="0591217"
configuracion_591_fp[17]="0591221"
configuracion_591_fp[18]="0591219"
configuracion_591_fp[19]="0591222"
configuracion_591_fp[20]="0591218"
configuracion_591_fp[21]="0591220"
configuracion_591_fp[22]="0591225"
configuracion_591_fp[23]="0591227"
configuracion_591_fp[24]="0591228"
configuracion_591_fp[25]="0591226"


expr_regular_codigo_centro=re.compile ( "^[0-9]{8}")
expr_regular_en_plantilla=re.compile("PLANTILLA")
nombre_fichero=sys.argv[1]
fichero=open(nombre_fichero, "r")
lineas=fichero.readlines()
fichero.close()

ANIO_PUBLICACION_PLANTILLA=sys.argv[2]

def generar_inserts(nombre_tabla, codigo_centro, tipo_plaza, cifras, configuracion):
    
    inserts=[]
    if (len(cifras)!=len(configuracion)):
        return []
    for i in range(0, len(configuracion)):
        lista_campos=ListaCampos.ListaCampos()
        cantidad=cifras[i]
        if cantidad==0:
            continue
        codigo_especialidad=configuracion[i]
        lista_campos.anadir("codigo_centro", codigo_centro)
        lista_campos.anadir("anio", ANIO_PUBLICACION_PLANTILLA, ListaCampos.ListaCampos.NUMERO)
        lista_campos.anadir("codigo_especialidad", codigo_especialidad)
        lista_campos.anadir("tipo_plaza", tipo_plaza)
        lista_campos.anadir("cantidad", cantidad, ListaCampos.ListaCampos.NUMERO)
        inserts.append ( lista_campos.generar_insert(nombre_tabla))
    return inserts
        
###############Programa principal###############33
i=0
sql=[]
configuracion_a_usar=[]
while i < len(lineas):
    
    (inicio_centro, fin_centro,codigo_centro)=utilidades.extraer_patron(
        expr_regular_codigo_centro, lineas[i])
    if (codigo_centro!=utilidades.PATRON_NO_ENCONTRADO):
        
        (inicio_plantilla, fin_plantilla, en_plantilla)= utilidades.extraer_patron(
                expr_regular_en_plantilla, lineas[i])
        
        
        #Plazas en plantilla
        linea_en_plantilla=lineas[i][fin_plantilla:].strip()
        cifras=utilidades.extraer_cifras_plantillas(linea_en_plantilla)
        if (len(cifras)==len(configuracion_590_comunes)):
            configuracion_a_usar=configuracion_590_comunes
        if (len(cifras)==len(configuracion_590_fp)):
            configuracion_a_usar=configuracion_590_fp
        if (len(cifras)==len(configuracion_591_fp)):
            configuracion_a_usar=configuracion_591_fp
            
        inserts=generar_inserts(GestorDB.NOMBRE_TABLA_PLANTILLAS,
                                codigo_centro, "PLANTILLA", cifras, configuracion_a_usar)
        sql+=inserts
        i=i+1
        #Plazas ocupadas
        linea_en_plantilla=lineas[i][fin_plantilla:].strip()
        cifras=utilidades.extraer_cifras_plantillas(linea_en_plantilla)
        inserts=generar_inserts(GestorDB.NOMBRE_TABLA_PLANTILLAS,
                                codigo_centro, "OCUPADA", cifras, configuracion_a_usar)
        sql+=inserts
        i=i+1
        #Plazas libres
        linea_en_plantilla=lineas[i][fin_plantilla:].strip()
        cifras=utilidades.extraer_cifras_plantillas(linea_en_plantilla)
        #print (linea_en_plantilla)
        inserts=generar_inserts(GestorDB.NOMBRE_TABLA_PLANTILLAS,
                                codigo_centro, "LIBRES", cifras, configuracion_a_usar)
        
        
        sql+=inserts
    i=i+1

for sentencia in sql:
    print (sentencia)
    
