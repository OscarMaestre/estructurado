#!/usr/bin/env python3
# coding=utf-8



import sys, os, re

from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import django
from django.db import transaction



class ProcesadorTablaDisponibles(object):
    def __init__(self, nombre_fichero, ClaseBolsas, codigo_cuerpo):
        self.codigo_cuerpo=codigo_cuerpo
        re_especialidad="Especialidad\s+[0-9]{3}"
        re_nombre_completo="  [A-ZÁÉÍÓÚÜÑ ]+, [A-ZÁÉÍÓÚÜÑ ]+"
        re_lista_provincias="[0-9]{2}( , [0-9]{2})*"
        self.expr_regular_nombre = re.compile ( re_nombre_completo )
        self.expr_regular_especialidad=re.compile ( re_especialidad )
        self.expr_regular_provincias=re.compile ( re_lista_provincias )
        self.bolsas=[]
        for tupla in ClaseBolsas.POSIBLES_BOLSAS:
            self.bolsas.append("("+tupla[0]+")")
        self.re_posible_bolsa="|".join(self.bolsas)
        self.re_posible_bolsa="("+ self.re_posible_bolsa +")"
        self.re_posible_bolsa += "\s+[0-9]{1,4}( |/|$)"
        self.expr_regular_bolsa=re.compile( self.re_posible_bolsa )
        self.procesador_pdf=ProcesadorPDF()
        self.fich_txt=self.procesador_pdf.convertir_a_txt ( nombre_fichero )
        #print ("Procesando {0}".format (fich_txt) )

    def con_ingles(self, linea):
        if linea[91:121].find("S")!=-1:
            return True
        return False
    
    def con_frances(self, linea):
        #print (linea)
        #print ("La linea mide "+len(linea))
        #print ("--"*20)
        if len(linea)<121:
            return False
        if linea[122:].find("S")!=-1:
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
    def construir_modelos(self, tupla):
        provincias=tupla[6].split(" , ")
        print (provincias)
        
    def procesar_tabla(self):
        self.procesador_pdf.abrir_fichero_txt ( self.fich_txt )
        especialidad=""
        while not self.procesador_pdf.eof():
            linea=self.procesador_pdf.get_linea_actual().strip()
            #Comprobamos si la linea contiene una especialidad
            (ini_espe, fin_espe, espe) = self.procesador_pdf.linea_contiene_patron(
                self.expr_regular_especialidad, linea)
            if espe!=self.procesador_pdf.PATRON_NO_ENCONTRADO:
                especialidad=espe[-3:]
                print ("Especialidad:"+especialidad)
            (ini_dni, fin_dni, dni)=self.procesador_pdf.linea_contiene_patron(
                self.procesador_pdf.expr_regular_dni, linea)
            if dni!=self.procesador_pdf.PATRON_NO_ENCONTRADO:
                num_orden=linea[:4].strip()
                (ini_bolsa, fin_bolsa, bolsa)=self.procesador_pdf.linea_contiene_patron(
                    self.expr_regular_bolsa, linea)
                if bolsa==self.procesador_pdf.PATRON_NO_ENCONTRADO:
                    print ("Error, bolsa no encontrada en esta linea")
                    print (linea)
                    linea=self.procesador_pdf.siguiente_linea()
                    continue
                tipo_bolsa=self.extraer_tipo_bolsa ( bolsa )
                orden_bolsa=self.extraer_orden_bolsa ( bolsa ) 
                nombre_completo=linea[fin_dni+1:ini_bolsa-1].strip()
                if nombre_completo=="":
                    linea_anterior=self.procesador_pdf.get_linea_anterior()
                    trozo1_de_nombre=linea_anterior[fin_dni+1:ini_bolsa-1].strip()
                    linea_siguiente=self.procesador_pdf.get_linea_siguiente()
                    trozo2_de_nombre=linea_siguiente[fin_dni+1:ini_bolsa-1].strip()
                    nombre = trozo1_de_nombre.strip() + " " + trozo2_de_nombre.strip()
                    print ("Nombre vacio! Quiza sea...")
                    print (nombre)
                    #print (linea)
                (ini_provincias, fin_provincias, lista_provincias)=self.procesador_pdf.linea_contiene_patron(
                    self.expr_regular_provincias, linea[fin_bolsa:])
                if lista_provincias==self.procesador_pdf.PATRON_NO_ENCONTRADO:
                    print("No se encontro ninguna provincia en la linea siguiente")
                    print (linea)
                    print ("Le presuponemos todas las provincias")
                    print ("-----------------------------------")
                    linea=self.procesador_pdf.siguiente_linea()
                    continue
                habla_ingles=self.con_ingles(linea)
                habla_frances=self.con_frances(linea)
                if True:
                    self.construir_modelos(
                        (num_orden, especialidad, dni, nombre_completo, tipo_bolsa,
                           orden_bolsa, lista_provincias, habla_ingles, habla_frances)
                    )
            self.procesador_pdf.siguiente_linea()
