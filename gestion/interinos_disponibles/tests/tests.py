#!/usr/bin/env python3
# coding=utf-8

import unittest, os
from utilidades.ficheros.GestorFicheros import GestorFicheros

PROCESADOR="procesar_tabla.py"

class TestDisponibles590_20160406(unittest.TestCase):
    def setUp(self):
        self.fichero="0590_20160406"
        self.gf=GestorFicheros()
        se
        self.gf.ejecutar_comando ( PROCESADOR, self.fichero )
        
    def testCuantosFrances(self):
        self.assertEqual(1,1)



if __name__ == '__main__':
    unittest.main()