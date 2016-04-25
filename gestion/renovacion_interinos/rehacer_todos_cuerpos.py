#!/usr/bin/env python3
# coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros
import platform

gf=GestorFicheros()

gf.ejecutar_comando("rm", "informes/*.pdf", "informes/*.rst", "informes/*.log")

#Estos son los tipos de centro que pueden pedir en primaria
gf.ejecutar_comando ("./generar_informes.py",
                     "CEIP", "CEE", "CEPA", "AEPA", "IES", "SES", "IESO")

gf.ejecutar_comando ("./generar_informes.py", "IES", "SES", "IESO", "CIFP")

gf.ejecutar_comando("rm", "informes/*.rst", "informes/*.log", "informes/*.out")