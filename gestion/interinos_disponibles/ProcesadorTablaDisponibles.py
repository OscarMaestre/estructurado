#!/usr/bin/env python3
# coding=utf-8



import sys, os, re
from utilidades.basedatos.Configurador import Configurador
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
import django
from django.db import transaction



print (re_posible_bolsa)

    
print (procesador_pdf.expr_regular_dni)


class ProcesadorTablaDisponible(object):
    def __init__(self, directorio, nombre_settings, nombre_fichero):
        self.configurador=Configurador ( directorio )
        self.configurador.activar_configuracion ( nombre_settings )
        from modelado_bd.models import *
        re_nombre_completo="  [A-ZÁÉÍÓÚÜÑ ]+, [A-ZÁÉÍÓÚÜÑ ]+"
        self.expr_regular_nombre = re.compile ( re_nombre_completo )
        
        self.bolsas=[]
        for tupla in InterinoDisponible.POSIBLES_BOLSAS:
            self.bolsas.append("("+tupla[0]+")")
        self.re_posible_bolsa="|".join(bolsas)
        self.re_posible_bolsa="("+ re_posible_bolsa +")"
        self.re_posible_bolsa += "\s+[0-9]{1,4}( |/|$)"
        self.expr_regular_bolsa=re.compile( re_posible_bolsa )
        self.procesador_pdf=ProcesadorPDF()
        self.fich_txt=procesador_pdf.convertir_a_txt ( nombre_fichero )
        print ("Procesando {0}".format (fich_txt) )

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

    def procesar_tabla(self):    
        self.procesador_pdf.abrir_fichero_txt ( self.fich_txt )
        while not self.procesador_pdf.eof():
            linea=self.procesador_pdf.get_linea_actual().strip()
            (ini_dni, fin_dni, dni)=self.procesador_pdf.linea_contiene_patron(
                self.procesador_pdf.expr_regular_dni, linea)
            if dni!=self.procesador_pdf.PATRON_NO_ENCONTRADO:
                num_orden=linea[:4].strip()
                (ini_bolsa, fin_bolsa, bolsa)=self.procesador_pdf.linea_contiene_patron(
                    expr_regular_bolsa, linea)
                if bolsa==self.procesador_pdf.PATRON_NO_ENCONTRADO:
                    print ("Error, bolsa no encontrada en esta linea")
                    print (linea)
                nombre_completo=linea[fin_dni+1:ini_bolsa-1].strip()
                if nombre_completo=="":
                    print ("Nombre vacio!")
                    print (linea)
                habla_ingles=con_ingles(linea)
                habla_frances=con_frances(linea)
                if habla_frances:
                    print (dni, nombre_completo, bolsa, habla_ingles, habla_frances)
            self.procesador_pdf.siguiente_linea()
