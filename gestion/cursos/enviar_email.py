#!/usr/bin/env python3
#coding=utf-8
import mysql.connector # sudo pip3 install mysql-connector-python
import sys, os
from utilidades.basedatos.Configurador import Configurador
import django
from django.db import transaction
from django.db.models import Q
configurador=Configurador (os.path.sep.join ([".."]) )

configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *


filtrado=Q(pago="Efectivo") | Q(pago="Transferencia")

inscripciones = InscripcionJornadas.objects.filter( filtrado )

for i in inscripciones:
    print (i)
