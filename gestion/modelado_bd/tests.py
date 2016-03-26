import unittest
from django.test import TestCase
import os
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *


# Create your tests here.

class TestAsignaciones(unittest.TestCase):
    def setUp(self):
        self.PROC_VACANTES_AGOSTO_2015="Vacantes 28-ago-2015"
    def test_cantidades_adjudicadas(self):
        #Se comprueban unas cuantas especialidades que hemos contado a mano en unos
        #cuantos procesos para ver si las adjudicaciones está
        
        #De la especialidad 0597021 debe haber 1
        nombramientos_esperados=1
        proc=ProcedimientoAdjudicacion.objects.get( nombre = self.PROC_VACANTES_AGOSTO_2015 )
        especialidad_asociada=Especialidad.objects.get("0597021")
        nombramientos_en_bd=Nombramiento.objects.filter(
            proceso=proc, especialidad=especialidad_asociada
        ).count()
        self.assertEquals( nombramientos_en_bd, nombramientos_esperados)