#!/usr/bin/env python3
#coding=utf-8
from utilidades.basedatos.Configurador import Configurador
from django.template.loader import render_to_string, get_template
from django.template.exceptions import TemplateDoesNotExist
from django.db.models import Q
from django.conf import settings

import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *


POS_AB=0
POS_CR=1
POS_CU=2
POS_GU=3
POS_TO=4

class Entrada(object):
    def __init__(self, numero, dni,
                 peticiones, posiciones, con_ingles, con_frances):
        self.numero         =   numero
        self.dni            =   dni
        self.posiciones     =   posiciones
        self.peticiones     =   peticiones
        self.con_ingles     =   con_ingles
        self.con_frances    =   con_frances
        
class GeneradorLista(object):
    def __init__(self, ClasePersona):
        self.ClasePersona=ClasePersona
        
    def get_personas_por_orden_bolsa(self,
            fichero_plantilla, codigo_especialidad):
        personas=self.ClasePersona.objects.all().order_by("orden_bolsa")
        #print (dir(personas[0]))
        personas=self.ClasePersona.objects.filter(
            especialidad__codigo_especialidad=codigo_especialidad).order_by("orden_bolsa")
        #print (personas[0])
        especialidad="0590"
        resultados=[]
        pos_ab=0
        pos_cr=0
        pos_cu=0
        pos_gu=0
        pos_to=0
        for p in personas:
            entrada=Entrada(
                p.orden_bolsa, p.dni,
                [p.elige_ab, p.elige_cr, p.elige_cu, p.elige_gu, p.elige_to],
                [pos_ab, pos_cr, pos_cu, pos_gu, pos_to],
                p.ingles, p.frances
            )
            if p.elige_ab:
                pos_ab=pos_ab+1
            if p.elige_cr:
                pos_cr=pos_cr+1
            if p.elige_cu:
                pos_cu=pos_cu+1
            if p.elige_gu:
                pos_gu=pos_gu+1
            if p.elige_to:
                pos_to=pos_to+1
            resultados.append(entrada)
        contexto={
            "personas":resultados,
            "especialidad":especialidad
        }
        cad=render_to_string(fichero_plantilla, contexto)
        print (cad)
        
            
            
if __name__ == '__main__':
    g=GeneradorLista(InterinoDisponible)
    g.get_personas_por_orden_bolsa("html_disponibles/plantilla_lista.html", "0590001")