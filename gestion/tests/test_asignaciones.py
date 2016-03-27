#!/usr/bin/env python3
#coding=utf-8
import unittest
import os
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador (os.path.sep.join ([".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *


# Create your tests here.

class TestAsignaciones(unittest.TestCase):
    def setUp(self):
        self.PROC_VACANTES_AGOSTO_2015=ProcedimientoAdjudicacion.VACANTES_28_08_2015
        self.PROC_VACANTES_SEP_2015_A=ProcedimientoAdjudicacion.VACANTES_08_09_2015
        self.PROC_VACANTES_SEP_2015_B=ProcedimientoAdjudicacion.VACANTES_18_09_2015
        self.SUSTIT_2015=ProcedimientoAdjudicacion.ASIGNACION_SUSTITUCIONES
    def verificar_proceso (self,
                nombre_proceso, cod_especialidad, cantidades_que_debe_haber):
        nombramientos_en_bd=Nombramiento.objects.filter(
            proceso__nombre=nombre_proceso,
            especialidad__codigo_especialidad=cod_especialidad
        ).count()
        mensaje_error="""
            \nProcedimiento {0} especialidad {1},
            esperados   -->{2: 4}<--
            encontrados -->{3: 4}<--
        """.format (nombre_proceso, cod_especialidad,
                    cantidades_que_debe_haber, nombramientos_en_bd)
            
        self.assertEqual( nombramientos_en_bd,
                         cantidades_que_debe_haber,
                         msg=mensaje_error)
        

    def test_generales(self):
        tuplas=[
            (self.PROC_VACANTES_AGOSTO_2015, "0590107", 17),
            (self.PROC_VACANTES_AGOSTO_2015, "0597021", 1),
            (self.PROC_VACANTES_AGOSTO_2015, "P590107", 10),
            (self.PROC_VACANTES_AGOSTO_2015, "0590101", 5),
            (self.PROC_VACANTES_AGOSTO_2015, "0596608", 1),
            (self.PROC_VACANTES_AGOSTO_2015, "0597021", 1),
            (self.PROC_VACANTES_AGOSTO_2015, "B590125", 1),
            (self.PROC_VACANTES_SEP_2015_B, "0591225", 12),
            (self.PROC_VACANTES_SEP_2015_A, "B597031", 14),
            (self.PROC_VACANTES_SEP_2015_A, "P597021", 2),
            (self.PROC_VACANTES_SEP_2015_A, "P597021", 2),
            (self.SUSTIT_2015+ "15-02-2016", "0591209", 1),
            (self.SUSTIT_2015+ "07-03-2016", "0597031", 6),
            (self.SUSTIT_2015+ "07-03-2016", "B597031", 2),
            (self.SUSTIT_2015+ "07-03-2016", "0597032", 3),
            (self.SUSTIT_2015+ "07-03-2016", "0597036", 5),
            (self.SUSTIT_2015+ "07-03-2016", "P597036", 2),
        ]
        for tupla in tuplas:
            proceso                 =   tupla[0]
            especialidad            =   tupla[1]
            cantidad_que_debe_haber =   tupla[2]
            self.verificar_proceso (
                proceso, especialidad, cantidad_que_debe_haber
            )
        
if __name__ == '__main__':
    unittest.main()