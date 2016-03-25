#!/usr/bin/python3


from subprocess import call
import platform
import os, sys


from utilidades.ficheros.GestorFicheros import GestorFicheros
import glob

gestor_fichero=GestorFicheros()

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
    
    

ficheros=["Convocadas_Interinos590", "Convocadas_Interinos591", 
          "Convocadas_Interinos594", "Convocadas_Interinos595",
          "NoConvocadas_Interinos0590", "NoConvocadas_Interinos0591", "NoConvocadas_Interinos0592", 
          "NoConvocadas_Interinos0594", "NoConvocadas_Interinos0595","NoConvocadas_Interinos0596",
          "ConvocadasMaestros", "NoConvocadasMaestros"]

ficheros=glob.glob("*.pdf")

for f in ficheros:
    if not gestor_fichero.existe_fichero(f[:-4]+".txt"):
        gestor_fichero.aplicar_comando(CONVERTIR, f)
    
for f in ficheros:
    gestor_fichero.aplicar_comando(PROCESAR, f[:-4]+".txt")
    




    
    
