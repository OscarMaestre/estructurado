#!/usr/bin/python3


from subprocess import call
import platform
import glob
import os, sys

from utilidades.ficheros.GestorFicheros import GestorFicheros
from utilidades.basedatos.GestorBD import GestorBD

gf=GestorFicheros()

CONVERTIR="pdftotext -layout -nopgbrk "

if (platform.system()=="Linux"):
    PROCESAR="./procesar_tabla.py "
    PROCESAR_MAESTROS="./procesar_tabla_maestros.py "
    BORRAR="rm "
if (platform.system()=="Windows"):
    PROCESAR="procesar_tabla.py "
    PROCESAR_MAESTROS="procesar_tabla_maestros.py "
    BORRAR="del "
    
FICH_RESULTADO="resultado.csv"
CONCAT="cat "

def procesar_directorio(anio):
    ficheros_pdf=glob.glob(anio+ os.sep + "*.pdf")
    print (ficheros_pdf)
    for f in ficheros_pdf:
        nuevo_nombre=gf.reemplazar_espacios(f)
        gf.renombrar_fichero(f, nuevo_nombre)
    
    ficheros_pdf=glob.glob(anio+ os.sep + "*.pdf")
    for f in ficheros_pdf:
        nombre_con_txt=f[:-4]+".txt"
        print (nombre_con_txt)
        if not gf.existe_fichero(nombre_con_txt):
            #print ("No existe:"+nombre_con_txt)    
            gf.aplicar_comando(CONVERTIR, f)
        
        
    gf.aplicar_comando(PROCESAR, anio+os.sep+"IES.txt", anio)
    gf.aplicar_comando(PROCESAR_MAESTROS, anio+os.sep+"Coles.txt", anio)

directorios=["2015", "2016"]
for anio in directorios:
    procesar_directorio(anio)
#gf.copiar_fichero( PROCESAR, " procesar_tabla.pytxt")
#gf.copiar_fichero("dodo.py", " dodo.pytxt")
    
    
