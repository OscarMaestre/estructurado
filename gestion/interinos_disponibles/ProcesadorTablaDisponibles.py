#!/usr/bin/env python3
# coding=utf-8



import sys, os, re

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import django
from django.db import transaction



class ProcesadorTablaDisponibles(object):
    def __init__(self, nombre_fichero,
                 codigo_cuerpo, ClaseInterino, ClaseEspecialidad):
        self.codigo_cuerpo=codigo_cuerpo
        self.ClaseInterino=ClaseInterino
        self.ClaseEspecialidad=ClaseEspecialidad
        re_especialidad="Especialidad\s+[0-9]{3}"
        re_nombre_completo="  [A-ZÁÉÍÓÚÜÑ ]+, [A-ZÁÉÍÓÚÜÑ ]+"
        re_lista_provincias="[0-9]{2}( , [0-9]{2})*"
        
        self.expr_regular_nombre = re.compile ( re_nombre_completo )
        self.expr_regular_especialidad=re.compile ( re_especialidad )
        self.expr_regular_provincias=re.compile ( re_lista_provincias )
        self.bolsas=[]
        for tupla in ClaseInterino.POSIBLES_BOLSAS:
            self.bolsas.append("("+tupla[0]+")")
        self.re_posible_bolsa="|".join(self.bolsas)
        self.re_posible_bolsa="("+ self.re_posible_bolsa +")"
        self.re_posible_bolsa += "\s+[0-9]{1,4}( |/|$)"
        self.expr_regular_bolsa=re.compile( self.re_posible_bolsa )
        self.procesador_pdf=ProcesadorPDF()
        self.fich_txt=self.procesador_pdf.convertir_a_txt ( nombre_fichero )
        #print ("Procesando {0}".format (fich_txt) )

    def con_ingles(self, linea, pos_palabra_ingles):
        if linea[pos_palabra_ingles:pos_palabra_ingles+6].find("S")!=-1:
            return True
        return False
    
    def con_frances(self, linea, pos_palabra_frances):
        if linea[pos_palabra_frances:].find("S")!=-1:
            return True
        return False
    
    def extraer_tipo_bolsa(self, bolsa):
        bolsa=bolsa.strip()
        tipo=bolsa[:3].strip()
        return tipo
    def extraer_orden_bolsa(self, bolsa):
        bolsa=bolsa.strip()
        orden=bolsa[4:].strip()
        return orden
    def get_modelo(self, tupla):
        provincias=tupla[6].split(" , ")
        quiere_ab=True if "02" in provincias else False
        quiere_cr=True if "13" in provincias else False
        quiere_cu=True if "16" in provincias else False
        quiere_gu=True if "19" in provincias else False
        quiere_to=True if "45" in provincias else False
        especialidad_relacionada=self.ClaseEspecialidad.objects.get(
            codigo_especialidad=self.codigo_cuerpo+tupla[1]
        )
        #print (especialidad_relacionada)
        i=self.ClaseInterino(
            orden=tupla[0], dni=tupla[2], nombre_completo=tupla[3],
            tipo_bolsa=tupla[4], orden_bolsa=tupla[5],
            elige_ab=quiere_ab, elige_cr=quiere_cr, elige_cu=quiere_cu,
            elige_gu=quiere_gu, elige_to=quiere_to,
            ingles=tupla[7], frances=tupla[8]
        )
        #m=self.get_modelo(
        #                (num_orden, especialidad, dni, nombre_completo, tipo_bolsa,
        #                   orden_bolsa, lista_provincias, habla_ingles, habla_frances)
        #            )
        #i.especialidad=especialidad_relacionada
        #print (tupla)
        
        return (i, especialidad_relacionada)
        
    def procesar_tabla(self):
        #Encontrar la columna donde está el inglés o el francés
        #requiere saber la posición donde empiezan estas palabras
        
        self.procesador_pdf.abrir_fichero_txt ( self.fich_txt )
        especialidad=""
        modelos=[]
        while not self.procesador_pdf.eof():
            linea=self.procesador_pdf.get_linea_actual()
            posible_pos_palabra_ingles=linea.find("Inglés")
            if posible_pos_palabra_ingles!=-1:
                pos_ingles=posible_pos_palabra_ingles
            posible_pos_palabra_frances=linea.find("Francés")
            if posible_pos_palabra_frances!=-1:
                pos_frances=posible_pos_palabra_frances
            #Comprobamos si la linea contiene una especialidad
            (ini_espe, fin_espe, espe) = self.procesador_pdf.linea_contiene_patron(
                self.expr_regular_especialidad, linea)
            if espe!=self.procesador_pdf.PATRON_NO_ENCONTRADO:
                especialidad=espe[-3:]
                #print ("Especialidad:"+especialidad)
            (ini_dni, fin_dni, dni)=self.procesador_pdf.linea_contiene_patron(
                self.procesador_pdf.expr_regular_dni, linea)
            if dni!=self.procesador_pdf.PATRON_NO_ENCONTRADO:
                num_orden=linea[:9].strip()
                (ini_bolsa, fin_bolsa, bolsa)=self.procesador_pdf.linea_contiene_patron(
                    self.expr_regular_bolsa, linea)
                if bolsa==self.procesador_pdf.PATRON_NO_ENCONTRADO:
                    print ("Error, bolsa no encontrada en esta linea")
                    print (linea)
                    linea=self.procesador_pdf.siguiente_linea()
                    continue
                tipo_bolsa=self.extraer_tipo_bolsa ( bolsa )
                orden_bolsa=self.extraer_orden_bolsa ( bolsa )
                #Por alguna razon, algunos numeros de orden
                #en bolsa llevan cosas como "263/1"
                orden_bolsa=orden_bolsa.replace("/", "")
                nombre_completo=linea[fin_dni+1:ini_bolsa-1].strip()
                if nombre_completo=="":
                    linea_anterior=self.procesador_pdf.get_linea_anterior()
                    trozo1_de_nombre=linea_anterior[fin_dni+1:ini_bolsa-1].strip()
                    linea_siguiente=self.procesador_pdf.get_linea_siguiente()
                    trozo2_de_nombre=linea_siguiente[fin_dni+1:ini_bolsa-1].strip()
                    nombre = trozo1_de_nombre.strip() + " " + trozo2_de_nombre.strip()
                    print ("Nombre vacio! Quiza sea...")
                    print (nombre)
                    nombre_completo=nombre
                    #print (linea)
                (ini_provincias, fin_provincias, lista_provincias)=self.procesador_pdf.linea_contiene_patron(
                    self.expr_regular_provincias, linea[fin_bolsa:])
                if lista_provincias==self.procesador_pdf.PATRON_NO_ENCONTRADO:
                    print("No se encontro ninguna provincia en la linea siguiente")
                    print (linea)
                    print ("Le presuponemos todas las provincias")
                    print ("-----------------------------------")
                    lista_provincias="02 , 13 , 16 , 19 , 45"
                habla_ingles=self.con_ingles(linea, pos_ingles)
                habla_frances=self.con_frances(linea, pos_frances)
                (m, esp)=self.get_modelo(
                        (num_orden, especialidad, dni, nombre_completo, tipo_bolsa,
                           orden_bolsa, lista_provincias, habla_ingles, habla_frances)
                )
                modelos.append( (m, esp) )
            self.procesador_pdf.siguiente_linea()
        #Fin del while
        with transaction.atomic():
            for tupla in modelos:
                (m,esp)=tupla
                m.save()
                m.especialidad.add (esp)
