#!/usr/bin/env python3
# coding=utf-8

import platform
import os, sys
DIR_UTILIDADES=".." + os.sep + "utilidades" + os.sep + "src"
sys.path.insert(0, DIR_UTILIDADES)
from utilidades.ficheros.GestorFicheros import GestorFicheros


FICHERO_CSV="centros_region.csv"
BD=".." + os.sep + ".." + os.sep + "docencia.db"
gf=GestorFicheros()

COMANDO_ECHO="echo"
comandos="""
.mode csv
.headers ON
select * from centros_region;
.quit
"""


if platform.system()=="Linux":
    COMANDO_ECHO = "echo \"{0}\"".format(comandos)
else:
    COMANDO_ECHO = "echo {0}".format(comandos)

gf.ejecutar_comando ( COMANDO_ECHO, "|", "sqlite3 " + BD, ">", FICHERO_CSV)