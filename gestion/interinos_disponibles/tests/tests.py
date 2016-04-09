#!/usr/bin/env python3
# coding=utf-8

import unittest, os
from utilidades.ficheros.GestorFicheros import GestorFicheros
from utilidades.basedatos.Configurador import Configurador
import sys, os
configurador=Configurador ( ".." + os.sep +".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
PROCESADOR="./procesar2.py"

class TestDisponibles590_20160406(unittest.TestCase):
    def setUp(self):
        self.fichero="0590_20160406.pdf"
        self.dir_actual=os.path.dirname(os.path.abspath(__file__))
        self.gf=GestorFicheros()
        self.procesar_fichero ( self.fichero , "0590")
        
    def procesar_fichero ( self, fichero, codigo_cuerpo ):
        os.chdir("..")
        self.gf.ejecutar_comando ( PROCESADOR,
            self.dir_actual+os.sep+self.fichero , codigo_cuerpo)
        
    def testCuantosFrances(self):
        cantidad_con_frances_en_bd=InterinoDisponible.objects.all().filter(frances=True).count()
        cantidad_con_frances_que_deberia_haber=10
        self.assertEqual(
            cantidad_con_frances_en_bd,
            cantidad_con_frances_que_deberia_haber)



if __name__ == '__main__':
    unittest.main()