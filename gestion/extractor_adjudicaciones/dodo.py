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

MODULO_GLOBAL="modulo.bas"
MODULO_LLAMADAS_PARCIALES="llamadas_generales"
adjudicaciones=["28-08-2015","08-09-2015","18-09-2015",
"02-10-2015","05-10-2015","07-10-2015",
"08-10-2015","13-10-2015","19-10-2015",
"26-10-2015","28-10-2015","02-11-2015",
"04-11-2015", "09-11-2015", "11-11-2015", "16-11-2015", "18-11-2015", "23-11-2015",
"25-11-2015", "30-11-2015", "02-12-2015", "09-12-2015", "14-12-2015", "11-01-2016", "13-01-2016",
"18-01-2016", "20-01-2016", "25-01-2016", "27-01-2016", "01-02-2016",
"03-02-2016", "10-02-2016", "15-02-2016", "17-02-2016", "22-02-2016", "24-02-2016", "29-02-2016",
"02-03-2016", "07-02-2016", "09-03-2016", "14-03-2016"]

EXTRACTOR="extractor.py "

if (platform.system()=="Linux"):
	PROCESAR="./procesar_tabla.py "
	EXTRACTOR="./extractor.py "
	BORRAR="rm "
if (platform.system()=="Windows"):
	PROCESAR="procesar_tabla.py "
	BORRAR="del "
	EXTRACTOR="extractor.py "


utilidades.borrar_fichero(MODULO_LLAMADAS_PARCIALES)
utilidades.borrar_fichero(MODULO_GLOBAL)




i=0
for f in adjudicaciones:
    i=i+1
    sufijo="{:0>3d}".format(i)
    nombre_macro="macros_"+sufijo+"_"+f
    if (platform.system()=="Linux"):
        utilidades.aplicar_comando(EXTRACTOR, f, " > "+nombre_macro)
    if (platform.system()=="Windows"):
        utilidades.aplicar_comando(EXTRACTOR, f, " > "+ nombre_macro)
    utilidades.concatenar_fichero(nombre_macro, MODULO_GLOBAL)
    

inicio="Public Function EjecutarGlobal()\n"
utilidades.anadir_a_fichero(inicio, MODULO_GLOBAL)

utilidades.concatenar_fichero(MODULO_LLAMADAS_PARCIALES, MODULO_GLOBAL)
fin="End Function\n"
utilidades.anadir_a_fichero(fin, MODULO_GLOBAL)
