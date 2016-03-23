#!/usr/bin/env python3
#coding=utf-8
import mysql.connector # sudo pip3 install mysql-connector-python
import sys, os
from utilidades.basedatos.Configurador import Configurador
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join ([".."]) )

configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *



USUARIO = sys.argv[1]
CLAVE   = sys.argv[2]
HOST    = sys.argv[3]
BD      = sys.argv[4]

CONSULTA="""
    select id, nif, apellido1, apellido2, nombre,
        email, telefono, anios_exp, especialidad, afiliado, forma_pago
            from matriculas_jornadas"""
cnx = mysql.connector.connect(user=USUARIO, password=CLAVE,
                              host=HOST,
                              database=BD)

inscripciones_ya_hechas=InscripcionJornadas.objects.all()

cursor=cnx.cursor()
cursor.execute (CONSULTA)
for f in cursor:
    identificador=f[0]
    print ("Examinando la inscripcion "+str(identificador))
    posible_inscripcion=InscripcionJornadas.objects.filter(id_inscripcion=identificador)
    if len(posible_inscripcion)==0:
        print ("Preinscribiendo la inscripcion "+str(identificador))
        i=InscripcionJornadas(
            id_inscripcion=f[0],
            nif=f[1], apellido1=f[2], apellido2=f[3], nombre=f[4],
            email=f[5], telefono=f[6], anios_exp=f[7], especialidad=f[8],
            afiliado=f[9], pago="Por procesar")
        i.save()
        
cnx.close()