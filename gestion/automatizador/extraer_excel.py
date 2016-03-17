#!/usr/bin/env python3
#coding=utf-8
import zipfile, os
from utilidades.ficheros.GestorFicheros import GestorFicheros
from bs4 import BeautifulSoup

path =os.path.dirname(os.path.abspath ( __file__ ))
gf=GestorFicheros()
zip_ref = zipfile.ZipFile("Afiliados.zip", 'r')
zip_ref.extractall(path)
zip_ref.close()
gf.borrar_fichero ( "Afiliados.zip")
descriptor_fichero=open ("Afiliados.xls", "r")
sopa = BeautifulSoup ( descriptor_fichero, "Afiliados.xls")