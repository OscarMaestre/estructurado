#!/usr/bin/python3


from subprocess import call
import platform
import os, sys

NUM_SUBDIRECTORIOS_ANTERIORES=1
SEPARADOR=os.sep

RUTA_PAQUETE_BD=(".."+SEPARADOR) * NUM_SUBDIRECTORIOS_ANTERIORES
DIRECTORIO= RUTA_PAQUETE_BD + "db_nombramientos"
#aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIRECTORIO)
import GestorDB
import utilidades
import glob

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
    if not utilidades.existe_fichero(f[:-4]+".txt"):
        utilidades.aplicar_comando(CONVERTIR, f)
    
for f in ficheros:
    utilidades.aplicar_comando(PROCESAR, f[:-4]+".txt", "> "+f+".res")
    
utilidades.borrar_fichero(FICH_RESULTADO)

for f in ficheros:
    utilidades.concatenar_fichero( f+".res", FICH_RESULTADO)


utilidades.copiar_fichero( PROCESAR, " procesar_tabla.pytxt")
utilidades.copiar_fichero("dodo.py", " dodo.pytxt")
    
    
