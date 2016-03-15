#!/usr/bin/python3



import platform
import glob
import os, sys

from utilidades.ficheros.GestorFicheros import GestorFicheros

gf=GestorFicheros()

CONVERTIR="pdftotext -layout -nopgbrk "

if (platform.system()=="Linux"):
    PROCESAR="./procesar_tabla.py "
    BORRAR="rm "
if (platform.system()=="Windows"):
    PROCESAR="procesar_tabla.py "
    BORRAR="del "
    
FICH_RESULTADO="resultado.csv"
CONCAT="cat "

ficheros_pdf=glob.glob("*.pdf")

for f in ficheros_pdf:
    nuevo_nombre=gf.reemplazar_espacios(f)
    gf.renombrar_fichero(f, nuevo_nombre)

ficheros_pdf=glob.glob("*.pdf")
for f in ficheros_pdf:
    nombre_con_txt=f[:-4]+".txt"
    if not gf.existe_fichero(nombre_con_txt):
        #print ("No existe:"+nombre_con_txt)    
        gf.aplicar_comando(CONVERTIR, f)
    
    
ficheros_txt=glob.glob("*.txt")
for f in ficheros_txt:
    gf.aplicar_comando(PROCESAR, f)  
    
