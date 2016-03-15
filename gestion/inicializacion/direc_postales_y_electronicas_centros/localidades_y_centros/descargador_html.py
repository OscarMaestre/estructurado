#!/usr/bin/env python3


import os, sys
DIR_UTILIDADES=".." + os.sep + "utilidades" + os.sep + "src"
sys.path.insert ( 0, DIR_UTILIDADES )
from utilidades.ficheros.GestorFicheros import GestorFicheros
from constantes import *

gf=GestorFicheros()
gf.crear_directorio ( SUBDIRECTORIO_HTML )

for i in range(0, TOTAL_PAGINAS):
    num = i*3
    url_descarga        = URL_BASE.format ( num )
    fichero_destino     = FICHERO_BASE.format ( i )
    if not gf.existe_fichero( fichero_destino ):
        gf.descargar_fichero(url_descarga, fichero_destino)