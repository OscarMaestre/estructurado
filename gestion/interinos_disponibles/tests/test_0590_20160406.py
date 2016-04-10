#!/usr/bin/env python3
# coding=utf-8

import unittest, os
from utilidades.ficheros.GestorFicheros import GestorFicheros
from interinos_disponibles.ProcesadorTablaDisponibles import ProcesadorTablaDisponibles

from django.test import TestCase
from modelado_bd.models import InterinoDisponible, Especialidad
from BaseDeTest import BaseDeTest

class TestDisponibles590_20160406(BaseDeTest):
    def setUp(self):
        self.procesar_fichero ( "0590_20160406.pdf" , "0590")            
    
    def test_sin_provincia(self):
         #Este caso no tenia ninguna provincia marcada, deberia tenerlas todas
         todos_sin_provincias=InterinoDisponible.objects.filter(dni__contains="65431W")
         uno_sin_provincias=todos_sin_provincias[0]
         self.assertEquals (
            True, uno_sin_provincias.elige_ab
         )
    def test_nombre_dividido(self):
        i=self.get_persona_dni_con ( "47742A" )
        #print ("Nombre:"+i.nombre_completo)
        pos_apellido_correcto=i.nombre_completo.find("ARANZUE")
        self.assertFalse (pos_apellido_correcto==-1)
    def test_con_ingles_y_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="84859H")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
        i=InterinoDisponible.objects.filter(dni__contains="90675S")[0]
        self.assertEquals (
            True, i.frances
         )
        self.assertEquals (
            True, i.ingles
        )
    def test_hablan_frances(self):
        i=InterinoDisponible.objects.filter(dni__contains="90675S")[0]
        self.assertEquals (
            True, i.frances
        )
        i=InterinoDisponible.objects.filter(dni__contains="24070Y")[0]
        self.assertEquals (
            True, i.frances
        )
        i=InterinoDisponible.objects.filter(dni__contains="94417E")[0]
        self.assertEquals (
            True, i.frances
        )
    def test_num_orden_con_barra(self):
        i=InterinoDisponible.objects.filter(dni__contains="739406P")[0]
        self.assertEquals (
            263, i.orden_bolsa
        )
    def test_especialidad(self):
        i=InterinoDisponible.objects.filter(dni__contains="27115S")[0]
        especialidades_asociadas=i.especialidad.all()
        especialidad=especialidades_asociadas[0]
        codigo_en_bd=especialidad.codigo_especialidad
        self.assertEquals(
            "0590005", codigo_en_bd
        )
    def testCuantosFrances(self):
        cantidad_con_frances_en_bd=InterinoDisponible.objects.all().filter(frances=True).count()
        cantidad_con_frances_que_deberia_haber=12
        self.assertEqual(
            cantidad_con_frances_en_bd,
            cantidad_con_frances_que_deberia_haber)



if __name__ == '__main__':
    unittest.main()