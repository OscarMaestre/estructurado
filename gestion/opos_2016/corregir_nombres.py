#!/usr/bin/env python3
#coding=utf-8
from utilidades.ficheros.GestorFicheros import GestorFicheros
modificaciones=[
    ("La Torre de Esteban Hambran", "Torre de Esteban Hambran"),
    ("Cortijos de Arriba", "Cortijo de Arriba"),
    ("Villafranca de los Caballeros", "Villafranca de los"),
    ("Las Ventas con Peña Aguilera", "Ventas Con Peña Aguilera")
]

gf=GestorFicheros()
sql_modificar_origen="update rutas set origen='{0}' where origen='{1}';"
sql_modificar_destino="update rutas set destino='{0}' where destino='{1}';"
ARCHIVO_BD="rutas.db"
for m in modificaciones:
    pueblo_antes=m[0]
    pueblo_como_debe_quedar=m[1]
    comando_sql_1=sql_modificar_origen.format (pueblo_antes, pueblo_como_debe_quedar)
    gf.ejecutar_comando(
        "echo \"" + comando_sql_1+ "\"", "| sqlite3 "+ARCHIVO_BD
    )
    comando_sql_2=sql_modificar_destino.format (pueblo_antes, pueblo_como_debe_quedar)
    gf.ejecutar_comando(
        "echo \"" + comando_sql_2+ "\"", "| sqlite3 "+ARCHIVO_BD
    )