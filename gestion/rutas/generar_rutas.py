#!/usr/bin/env python3
# coding=utf-8

from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
import sys, os

from django.template.loader import render_to_string, get_template


if __name__ == '__main__':
    configurador=Configurador ( ".." )
    configurador.activar_configuracion ( "gestion.settings" )
    from modelado_bd.models import *
    gestor_bd=GestorBD("rutas.db")
    localidades=Localidad.objects.all()
    for l in localidades:
        codigo_loc=l.codigo_localidad
        nombre_loc=l.nombre_localidad
        sql="select origen, destino, minutos, distancia from rutas where origen='{0}'".format(nombre_loc)
        #print (sql)
        filas=gestor_bd.get_filas ( sql )
        if len(filas)!=0:
            resultado=filas[0]
            #print (len(codigo_loc), codigo_loc)
        else:
            if len(filas)==0:
                print ("Localidad no encontrada:"+nombre_loc)