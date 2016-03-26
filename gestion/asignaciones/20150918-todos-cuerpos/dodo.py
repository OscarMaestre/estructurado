#!/usr/bin/python3


from subprocess import call
import platform
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
def aplicar_comando (comando, fichero, *args):
    cmd=comando + fichero
    for a in args:
        cmd+=" " + a
    print("Ejecutando "+cmd)
    call(cmd, shell=True)
    
    

ficheros=["0590", "0591", "0592", "0594", "0595", "0596", "0597"]



for f in ficheros:
    if not gf.existe_fichero(f+".txt"):
        gf.aplicar_comando(CONVERTIR, f+".pdf")
    
for f in ficheros:
    gf.aplicar_comando(PROCESAR, f+".txt")
    

    
