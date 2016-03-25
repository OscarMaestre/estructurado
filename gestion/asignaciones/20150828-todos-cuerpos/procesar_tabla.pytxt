#!/usr/bin/env python3


import re
import sys
import string
import os

NUM_SUBDIRECTORIOS_ANTERIORES=1
SEPARADOR=os.sep

RUTA_PAQUETE_BD=(".."+SEPARADOR) * NUM_SUBDIRECTORIOS_ANTERIORES
DIRECTORIO= RUTA_PAQUETE_BD + "db_nombramientos"

#aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIRECTORIO)
import GestorDB
import ListaCampos
import utilidades


archivo=sys.argv[1]
re_dni="[0-9]{7,8}[A-Z]"
#especialidad="[PWB0]59[0-9][0-9]{3}"
re_especialidad="[FRPWB0]59([0-9]{4})"
re_codigo_centro="[0-9]{8}"
re_codigo_centro_ciudad_real="^13[0-9]{6}$"
re_fecha="[0-9]{2}/[0-9]{2}/[0-9]{4}"

def linea_contiene_patron(patron, linea):
    expresion=re.compile(patron)
    if expresion.search(linea):
        return True
    return False


def extraer_patron(patron, linea):
    
    expresion=re.compile(patron)
    concordancia=expresion.search(linea)
    if concordancia:
        inicio=concordancia.start()
        final=concordancia.end()
        return concordancia.string[inicio:final]
    return "No concordancia"



def extraer_codigo_centro(linea):
    return extraer_patron(re_codigo_centro, linea)

def extraer_localidad(linea):
    localidad=linea[9:51]
    return localidad.strip()

def extraer_dni(linea):
    trozo=linea[51:60]
    return extraer_patron(re_dni, linea)

def extraer_nombre(linea):
    linea=linea[49:]
    pos=string.find(linea, "-")
    if pos==-1:
        return "Error:"+linea
    return linea[pos+2:].strip()
    
    
cadena_sql="""insert into asignaciones_18092015 values
                    (
                        *C1*'{0}'*C1*,
                        *C2*'{1}'*C2*,
                        *C3*'{2}'*C3*,
                        *C4*'{3}'*C4*,
                        *C5*'{4}'*C5*,
                        *C6*'{5}'*C6*,
                        *C7*'{6}'*C7*,
                        *C8*'{7}'*C8*
                        
                    );
                    
                  """
def generar_linea_sql(lista_campos):
    dni=lista_campos[0]
    cod_centro=lista_campos[3]
    if not linea_contiene_patron(re_codigo_centro_ciudad_real, cod_centro):
        cod_centro="9888"
    sql= "update gaseosa set cod_centro='"+cod_centro+"' where dni='"+dni+"';\n"
    sql+="update gaseosa set auxiliar='VACANTE TODO CURSO 15/16' where dni='"+dni+"';\n"
    return sql
                                        
def generar_linea_sql2(lista_campos):
    valores=":".join(lista_campos)
    return valores

archivo=open(archivo,"r", encoding="utf-8")
lineas=archivo.readlines()
total_lineas=len(lineas)
codigo_especialidad=""
lista_inserts_sql3=[]
for i in range(0, total_lineas):
    lista_campos_para_insertar=ListaCampos.ListaCampos()
    linea=lineas[i]
    if i+1==total_lineas:
        break
    linea_siguiente=lineas[i+1]
    lista_campos=[]
    if (linea_contiene_patron(re_dni, linea_siguiente)):
        dni=extraer_patron(re_dni, linea_siguiente)
        
        nombre_centro=linea_siguiente[28:61].strip()
        
        nombre_persona=linea[:32].strip()
        
        codigo_centro=extraer_codigo_centro(linea[27:64])
        
        codigo_especialidad=extraer_patron(re_especialidad, linea[49:86])
        
        nombre_localidad=linea_siguiente[94:].strip()
        lista_campos.append(dni)
        lista_campos_para_insertar.anadir("nif", dni, ListaCampos.ListaCampos.CADENA)
        lista_campos.append(nombre_persona)
        lista_campos_para_insertar.anadir("nombre_completo", nombre_persona, ListaCampos.ListaCampos.CADENA)
        lista_campos.append(codigo_especialidad)
        lista_campos_para_insertar.anadir("especialidad", codigo_especialidad, ListaCampos.ListaCampos.CADENA)
        lista_campos_para_insertar.anadir("fecha_inicio", "2015-09-01", ListaCampos.ListaCampos.CADENA)
        lista_campos_para_insertar.anadir("fecha_fin", "2016-06-24", ListaCampos.ListaCampos.CADENA)
        lista_campos.append(codigo_centro)
        lista_campos_para_insertar.anadir("fecha_procedimiento", "2015-08-28")
        lista_campos_para_insertar.anadir("codigo_centro", codigo_centro, ListaCampos.ListaCampos.CADENA)
        lista_campos_para_insertar.anadir("procedimiento", "Adjudicacion 28-08-2015", ListaCampos.ListaCampos.CADENA)
        lista_campos.append(nombre_centro)
        lista_campos.append(nombre_localidad)
        sql=generar_linea_sql(lista_campos)
        lista_inserts_sql3.append(lista_campos_para_insertar.generar_insert("nombramientos"))
        print(sql)
        continue
    else:
        continue
    

    
archivo.close()
GestorDB.BD_RESULTADOS.ejecutar_sentencias(lista_inserts_sql3)