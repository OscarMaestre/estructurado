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
        self.procesar_fichero ( "0597_20160406.pdf" , "0597")            
    
    def test_con_ingles(self):
        i=self.get_persona_dni_con("130984V")
        self.assertEquals (
            True, i.ingles
        )
        i=self.get_persona_dni_con("246731M")
        self.assertEquals (
            True, i.ingles
        )
        i=self.get_persona_dni_con("229089K")
        self.assertEquals (
            True, i.ingles
        )
    def test_con_ingles_y_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="215442Z")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
        i=InterinoDisponible.objects.filter(dni__contains="392225V")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
        i=InterinoDisponible.objects.filter(dni__contains="600020C")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
        i=InterinoDisponible.objects.filter(dni__contains="1673361W")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
        
        
    def test_hablan_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="69826R")[0]
        self.assertEquals (
            True, i.frances
        )
        i=InterinoDisponible.objects.filter(dni__contains="73837L")[0]
        self.assertEquals (
            True, i.frances
        )
        i=InterinoDisponible.objects.filter(dni__contains="908651C")[0]
        self.assertEquals (
            True, i.frances
        )
        
        
    def test_bolsa(self):
        personas=self.get_toda_persona_dni_con("84859H")
        for i in personas:
            if i.bolsa=="R1G":
                self.assertEquals ( "R1G", i.bolsa)
            if i.bolsa=="P1":
                self.assertEquals ( "P1", i.bolsa)
    def test_especialidad(self):
        tiene_espe=self.dni_tiene_especialidad(
            "40473W", "0597072"
        )
        self.assertEquals ( True, tiene_espe )
    
if __name__ == '__main__':
    unittest.main()