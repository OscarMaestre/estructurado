#!/usr/bin/env python3
# coding=utf-8

from utilidades.basedatos.Configurador import Configurador
import sys, os
from GeneradorLista import GeneradorLista
from django.template.loader import render_to_string, get_template


especialidades_excluidas=["0597777"]
cuerpos=[
    ("0597", "Maestros"),
    ("0590", "Secundaria"),
    ("0591", "Profesores Técnicos de FP"),
    ("0592", "Escuelas Oficiales de Idiomas"),
    ("0594", "Conservatorios"),
    ("0595", "Escuelas de Artes"),
    ("0596", "Maestros de taller artes plásticas"),
]

def generar_lista_cuerpo(generador, especialidades):
    
    for e in especialidades:
        if e.codigo_especialidad in especialidades_excluidas:
            continue
        print (e.codigo_especialidad)
        generador.generar_lista_html("html_disponibles/plantilla_lista.html",
                    e.codigo_especialidad, e.descripcion    ,
                    directorio_salida + e.codigo_especialidad + ".html")


directorio_salida="resultados" +os.sep
pagina_index=directorio_salida +  "index_cuerpo.html"
if __name__ == '__main__':
    configurador=Configurador ( ".." )
    configurador.activar_configuracion ( "gestion.settings" )
    from modelado_bd.models import *
    
    
    for tupla in cuerpos:
        (codigo_cuerpo, nombre_cuerpo)=tupla
        g=GeneradorLista(InterinoDisponible)
        especialidades=Especialidad.objects.filter(
            codigo_especialidad__startswith=codigo_cuerpo).order_by(
            "codigo_especialidad")
        generar_lista_cuerpo ( g, especialidades )
        contexto={
            "codigo_cuerpo":codigo_cuerpo,
            "nombre_cuerpo":nombre_cuerpo,
            "especialidades":especialidades
        }
        fichero_html_de_cuerpo=directorio_salida + "index{0}.html".format(codigo_cuerpo)
        cad=render_to_string("html_disponibles/index_cuerpo.html", contexto)
        descriptor=open(fichero_html_de_cuerpo, "w")
        descriptor.write (cad)
        descriptor.close()