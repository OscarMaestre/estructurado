#!/usr/bin/env python3
#coding=utf-8


from utilidades.basedatos.Configurador import Configurador
from utilidades.modelos.Modelos import get_directorio_archivos_especialidades,extraer_tuplas_especialidades_de_fichero
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *



def crear_todas_especialidades(codigo_cuerpo, crear_bolsas_asociadas=False):
    f=codigo_cuerpo
    sql=[]
    dir_datos=get_directorio_archivos_especialidades()
    ruta_fichero=dir_datos+os.path.sep+"Especialidades0{0}.txt".format(f)
    especialidades=extraer_tuplas_especialidades_de_fichero( ruta_fichero )
    lista_especialidades_a_insertar=[]
    for tupla in especialidades:
        codigo_especialidad_extraida=tupla[0]
        nombre=tupla[1]
        exige_bilingue_ingles=True
        no_exige_bilingue_ingles=False
        exige_bilingue_frances=True
        no_exige_bilingue_frances=False
        es_a_tiempo_parcial=True
        no_es_a_tiempo_parcial=False
        #Creamos todas las especialidades con todas las combinaciones
        #de ingles y frances
        
        #0590107 es 0(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="0"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_ESPANOL,
            tipo_de_jornada=Especialidad.JORNADA_COMPLETA
        )
        especialidad.save()
        #P590107 es P(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="P"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_ESPANOL,
            tipo_de_jornada=Especialidad.MEDIA_JORNADA
        )
        especialidad.save()
        
        #B590107 es B(Tiempo completo, bilingüe inglés) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="B"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_INGLES,
            tipo_de_jornada=Especialidad.JORNADA_COMPLETA
        )
        especialidad.save()
        
        #W590107 es W(Tiempo parcial, bilingüe inglés) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="W"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_INGLES,
            tipo_de_jornada=Especialidad.MEDIA_JORNADA
        )
        especialidad.save()
        
        #F590107 es F(Tiempo completo, bilingüe francés) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="F"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_FRANCES,
            tipo_de_jornada=Especialidad.JORNADA_COMPLETA
        )
        especialidad.save()
        
        #R590107 es R(Tiempo parcial, bilingüe francés) 590 Secund 107 Informatica
        especialidad=Especialidad(
            codigo_especialidad="R"+codigo_cuerpo+codigo_especialidad_extraida,
            descripcion=nombre,
            idioma=Especialidad.IDIOMA_FRANCES,
            tipo_de_jornada=Especialidad.MEDIA_JORNADA
        )
        especialidad.save()
        
        
with transaction.atomic():
    cuerpos=["590", "591", "592", "594", "595", "511","597", "596"]
    for cuerpo in cuerpos:
        crear_todas_especialidades( cuerpo )
