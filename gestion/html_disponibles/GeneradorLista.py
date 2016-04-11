#!/usr/bin/env python3
#coding=utf-8
from utilidades.basedatos.Configurador import Configurador
from django.template.loader import render_to_string, get_template
from django.template.exceptions import TemplateDoesNotExist
from django.db.models import Q
from django.conf import settings
from copy import copy
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *


POS_AB=0
POS_CR=1
POS_CU=2
POS_GU=3
POS_TO=4


class Posiciones(object):
    def __init__(self):
        self.POS_AB_SIN_IDIOMA  =   1
        self.POS_CR_SIN_IDIOMA  =   1
        self.POS_CU_SIN_IDIOMA  =   1
        self.POS_GU_SIN_IDIOMA  =   1
        self.POS_TO_SIN_IDIOMA  =   1
        
        self.POS_AB_CON_INGLES  =   1
        self.POS_CR_CON_INGLES  =   1
        self.POS_CU_CON_INGLES  =   1
        self.POS_GU_CON_INGLES  =   1
        self.POS_TO_CON_INGLES  =   1
        
        self.POS_AB_CON_FRANCES  =   1
        self.POS_CR_CON_FRANCES  =   1
        self.POS_CU_CON_FRANCES  =   1
        self.POS_GU_CON_FRANCES  =   1
        self.POS_TO_CON_FRANCES  =   1
        
        
        
class Entrada(object):
    def __init__(self, persona, posiciones):
        self.persona=persona
        self.posiciones=copy ( posiciones )
        
class GeneradorLista(object):
    def __init__(self, ClasePersona):
        self.ClasePersona=ClasePersona
        
    def get_personas_por_orden_bolsa(self,
            fichero_plantilla, codigo_especialidad):
        
        posiciones = Posiciones()
        
        personas=self.ClasePersona.objects.all().order_by("orden_bolsa")
        #print (dir(personas[0]))
        personas=self.ClasePersona.objects.filter(
            especialidad__codigo_especialidad=codigo_especialidad).order_by("orden_bolsa")
        #print (personas[0])
        especialidad="0590"
        resultados=[]
        
        for p in personas:
            entrada=Entrada(
                p, posiciones
            )
            if p.elige_ab:
                posiciones.POS_AB_SIN_IDIOMA+=1
                if p.ingles:
                    posiciones.POS_AB_CON_INGLES+=1
                if p.frances:
                    posiciones.POS_AB_CON_FRANCES+=1
            if p.elige_cr:
                posiciones.POS_CR_SIN_IDIOMA+=1
                if p.ingles:
                    posiciones.POS_CR_CON_INGLES+=1
                if p.frances:
                    posiciones.POS_CR_CON_FRANCES+=1
            if p.elige_cu:
                posiciones.POS_CU_SIN_IDIOMA+=1
                if p.ingles:
                    posiciones.POS_CU_CON_INGLES+=1
                if p.frances:
                    posiciones.POS_CU_CON_FRANCES+=1
            if p.elige_gu:
                posiciones.POS_GU_SIN_IDIOMA+=1
                if p.ingles:
                    posiciones.POS_GU_CON_INGLES+=1
                if p.frances:
                    posiciones.POS_GU_CON_FRANCES+=1
            if p.elige_to:
                posiciones.POS_TO_SIN_IDIOMA+=1
                if p.ingles:
                    posiciones.POS_TO_CON_INGLES+=1
                if p.frances:
                    posiciones.POS_TO_CON_FRANCES+=1
            resultados.append(entrada)
        contexto={
            "personas":resultados,
            "especialidad":especialidad
        }
        cad=render_to_string(fichero_plantilla, contexto)
        print (cad)
        
            
            
if __name__ == '__main__':
    g=GeneradorLista(InterinoDisponible)
    g.get_personas_por_orden_bolsa("html_disponibles/plantilla_lista.html", "0597031")