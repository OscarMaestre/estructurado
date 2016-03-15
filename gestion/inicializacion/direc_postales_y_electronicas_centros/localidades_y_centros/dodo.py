#!/usr/bin/env python3
#coding=utf-8
import os, sys


DIR_UTILIDADES=".." + os.sep + "utilidades" + os.sep + "src"
print (DIR_UTILIDADES)


sys.path.insert(0, DIR_UTILIDADES)
from utilidades.ficheros.GestorFicheros import GestorFicheros
gf=GestorFicheros()

gf.ejecutar_comando("./descargador_html.py", "")
gf.ejecutar_comando("./procesador_centros.py", ">", "centros_region.sql")
gf.ejecutar_comando ("cat centros_region.sql", "|", "sqlite3 ../../docencia.db")
