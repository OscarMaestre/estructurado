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
        self.PROC_VACANTES_SEP_2015=ProcedimientoAdjudicacion.VACANTES_18_09_2015
    def test_asignacion_maestros_no_convocadas_ant_logse_28_08_2015(self):
        #Se comprueban unas cuantas especialidades que hemos contado a mano en unos
        #cuantos procesos para ver si las adjudicaciones está bien
        
        procesos=[
            self.PROC_VACANTES_SEP_2015
        ]
        especialidades_en_esos_procesos=[
            "0591224"
        ]
        cantidades_esperadas_de_adjudicaciones=[
            1
        ]
        
        for i in range (0, len(procesos)):
            nombre_proceso              =   procesos[i]
            cod_especialidad            =   especialidades_en_esos_procesos[i]
            cantidades_que_debe_haber   =   cantidades_esperadas_de_adjudicaciones[i]
            
            
            nombramientos_en_bd=Nombramiento.objects.filter(
                proceso__nombre=nombre_proceso,
                especialidad__codigo_especialidad=cod_especialidad
            ).count()
            self.assertEqual( nombramientos_en_bd, cantidades_que_debe_haber)
        
if __name__ == '__main__':
    unittest.main()