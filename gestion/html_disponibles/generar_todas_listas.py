#!/usr/bin/env python3
# coding=utf-8

from utilidades.basedatos.Configurador import Configurador
import sys, os
from GeneradorLista import GeneradorLista
from django.template.loader import render_to_string, get_template

directorio_salida="resultados" +os.sep
pagina_index=directorio_salida +  "index.html"
if __name__ == '__main__':
    configurador=Configurador ( ".." )
    configurador.activar_configuracion ( "gestion.settings" )
    from modelado_bd.models import *
    g=GeneradorLista(InterinoDisponible)
    especialidades=Especialidad.objects.filter(codigo_especialidad__startswith="059").order_by("codigo_especialidad")
    for e in especialidades:
        if e.codigo_especialidad=="0597777":
            continue
        print (e.codigo_especialidad)
        g.get_personas_por_orden_bolsa("html_disponibles/plantilla_lista.html",
                    e.codigo_especialidad, e.descripcion    ,
                    directorio_salida + e.codigo_especialidad + ".html")
    
    contexto={
        "especialidades":especialidades
    }
    cad=render_to_string("html_disponibles/index.html", contexto)
    descriptor=open(pagina_index, "w")
    descriptor.write (cad)
    descriptor.close()