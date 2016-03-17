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
#gf.borrar_fichero ( "Afiliados.zip")
descriptor_fichero=open ("Afiliados.xls", "r")
gf.renombrar_fichero ( "Afiliados.xls", "Afiliados.html")
fichero=open("Afiliados.html")
sopa = BeautifulSoup ( fichero, "html.parser")

tbody=sopa.find("tbody")
filas=tbody.find_all("tr")
for fila in filas:
    celdas=fila.find_all("td")
    dni         =   celdas[0].text
    nombre      =   celdas[2].text
    ap1         =   celdas[3].text
    ap2         =   celdas[4].text
    email       =   celdas[6].text
    sexo        =   celdas[8].text
    fecha_nac   =   celdas[9].text
    domicilio   =   celdas[10].text
    localidad   =   celdas[11].text
    cp          =   celdas[12].text
    provincia   =   celdas[13].text
    tlf_fijo    =   celdas[14].text
    tlf_movil   =   celdas[15].text
    fecha_alta  =   celdas[17].text
    iban        =   celdas[29].text
    num_entidad =   celdas[30].text
    num_sucur   =   celdas[31].text
    dc          =   celdas[32].text
    ccc         =   celdas[33].text
    num_nuestro_estilo = num_entidad + num_sucur + dc + ccc
    
    print (dni, ap1, ap2, nombre, email, sexo, fecha_nac,
           domicilio, localidad, cp, provincia, tlf_fijo, tlf_movil,
           iban, num_nuestro_estilo)
