#!/usr/bin/env python3
#coding=utf-8

from django.test import TestCase
from interinos_disponibles.ProcesadorTablaDisponibles import ProcesadorTablaDisponibles
from modelado_bd.models import InterinoDisponible, Especialidad

import os
class BaseDeTest(TestCase):
    def procesar_fichero (self, nombre_fichero, codigo_cuerpo):
        self.fichero=nombre_fichero
        self.dir_actual=os.path.dirname(os.path.abspath(__file__))
        #print (self.dir_actual)
        Especialidad.crear_todas_especialidades()
        procesador=ProcesadorTablaDisponibles(
            self.dir_actual + os.sep + self.fichero,  codigo_cuerpo,
            InterinoDisponible, Especialidad )

        procesador.procesar_tabla()
    def get_persona_dni_con(self, cadena):
        i=InterinoDisponible.objects.filter(dni__contains=cadena)[0]
        return i
    def get_toda_persona_dni_con(self, cadena):
        i=InterinoDisponible.objects.filter(dni__contains=cadena)
        return i
    
    def dni_tiene_especialidad(self, dni, codigo_especialidad):
        i=self.get_persona_dni_con(dni)
        especialidades_que_tiene=especialidades_asociadas=i.especialidad.all()
        for e in especialidades_que_tiene:
            if codigo_especialidad==e.codigo_especialidad:
                return True
        return False
    