#!/usr/bin/python3


from subprocess import call
import platform
import glob
import os, sys

NUM_SUBDIRECTORIOS_ANTERIORES=2
SEPARADOR=os.sep

RUTA_PAQUETE_BD=(".."+SEPARADOR) * NUM_SUBDIRECTORIOS_ANTERIORES
DIRECTORIO= RUTA_PAQUETE_BD + os.sep + "utilidades" + os.sep + "src"
#aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIRECTORIO)

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
    
    
gf.aplicar_comando(PROCESAR, "590-Medias.txt", "2016")
gf.aplicar_comando(PROCESAR_MAESTROS, "597-Maestros.txt", "2016")


#gf.copiar_fichero( PROCESAR, " procesar_tabla.pytxt")
#gf.copiar_fichero("dodo.py", " dodo.pytxt")
    
    
