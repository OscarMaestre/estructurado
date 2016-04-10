#!/usr/bin/env python3
# coding=utf-8

import unittest, os
from utilidades.ficheros.GestorFicheros import GestorFicheros
from interinos_disponibles.ProcesadorTablaDisponibles import ProcesadorTablaDisponibles

from django.test import TestCase
from modelado_bd.models import InterinoDisponible, Especialidad
from BaseDeTest import BaseDeTest

class TestDisponibles591_20160406(BaseDeTest):
    def setUp(self):
        self.procesar_fichero ( "0591_20160406.pdf" , "0591")            
    
    def test_sin_provincia(self):
         #Este caso no tenia ninguna provincia marcada, deberia tenerlas todas
         todos_sin_provincias=InterinoDisponible.objects.filter(dni__contains="25399R")
         uno_sin_provincias=todos_sin_provincias[0]
         self.assertEquals (
            True, uno_sin_provincias.elige_ab
         )
         self.assertEquals (
            True, uno_sin_provincias.elige_cr
         )
         self.assertEquals (
            True, uno_sin_provincias.elige_cu
         )
         self.assertEquals (
            True, uno_sin_provincias.elige_gu
         )
         self.assertEquals (
            True, uno_sin_provincias.elige_to
         )
    def test_con_ingles(self):
        i=self.get_persona_dni_con("518491P")
        self.assertEquals (
            True, i.ingles
        )
    def test_con_ingles_y_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="073858B")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
    def test_hablan_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="659907K")[0]
        self.assertEquals (
            True, i.frances
        )
        i=InterinoDisponible.objects.filter(dni__contains="073858B")[0]
        self.assertEquals (
            True, i.frances
        )
        
    
    def test_especialidad(self):
        si_tiene_la_0591227=self.dni_tiene_especialidad(
            "151519W", "0591227"
        )
        self.assertEquals ( True, si_tiene_la_0591227 )
    
if __name__ == '__main__':
    unittest.main()