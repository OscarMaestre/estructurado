#!/usr/bin/env python3
#coding=utf-8
from utilidades.basedatos.Configurador import Configurador
from django.template.loader import render_to_string, get_template
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings

import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *

class GeneradorLista(object):
    def __init__(self, ClasePersona):
        self.ClasePersona=ClasePersona
        
    def get_personas_por_orden_bolsa(self, fichero_plantilla):
        i=self.ClasePersona.objects.all()
        especialidad="0590"
        contexto={
            "personas":i,
            "especialidad":especialidad
        }
        cad=render_to_string(fichero_plantilla, contexto)
        print (cad)
        
            
            
if __name__ == '__main__':
    g=GeneradorLista(InterinoDisponible)
    g.get_personas_por_orden_bolsa("html_disponibles/plantilla_lista.html")