#!/usr/bin/env python3
# coding=utf-8

import csv

from utilidades.basedatos.Configurador import Configurador
import os
import sys
import django
from django.db import transaction
configurador=Configurador (os.path.sep.join (["..", ".."]) )
configurador.activar_configuracion ( "gestion.settings")
from modelado_bd.models import *


class ProcesadorCSVGaseosa(object):
    CAMPO_NO_LOCALIZADO=-1
    CORRESPONDENCIA=dict()
    CORRESPONDENCIA["DNI"]="dni"
    CORRESPONDENCIA["APELLIDO 1"]="apellido_1"
    CORRESPONDENCIA["APELLIDO 2"]="apellido_2"
    CORRESPONDENCIA["NOMBRE"]="nombre"
    CORRESPONDENCIA["Dirección"]="direccion"
    CORRESPONDENCIA["C_Postal"]="codigo_postal"
    CORRESPONDENCIA["Ciudad"]="ciudad"
    CORRESPONDENCIA["Provincia"]="provincia"
    CORRESPONDENCIA["Email"]="email"
    CORRESPONDENCIA["F_nace"]="fecha_nacimiento"
    CORRESPONDENCIA["Cuota"]="cuota"
    CORRESPONDENCIA["Tfno_Casa"]="tlf_casa"
    CORRESPONDENCIA["Tfno_Móvil"]="tlf_movil"
    CORRESPONDENCIA["F_Alta"]="fecha_alta"
    CORRESPONDENCIA["F_Baja"]="fecha_baja"
    CORRESPONDENCIA["CodCentroDefinitivo"]="cod_centro_def"
    CORRESPONDENCIA["CodCentroCursoActual"]="cod_centro_actual"
    CORRESPONDENCIA["Auxiliar"]="auxiliar"
    CORRESPONDENCIA["Cuerpo"]="cuerpo"
    CORRESPONDENCIA["Espec 1"]="especialidad"
    CORRESPONDENCIA["IBAN"]="iban"
    CORRESPONDENCIA["Cuenta"]="ccc"
    CORRESPONDENCIA["SEXO"]="sexo"
    def __init__(self):
        self.posiciones_campos=dict()
        self.posiciones_campos["DNI"]        = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["APELLIDO 1"] = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["APELLIDO 2"] = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["NOMBRE"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["SEXO"]       = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Dirección"]  = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["C_Postal"]   = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Ciudad"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Provincia"]  = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Email"]      = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["F_nace"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Cuota"]      = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Tfno_Casa"]  = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Tfno_Móvil"] = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["F_Alta"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["F_Baja"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Cuerpo"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Espec 1"]     = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        
        self.posiciones_campos["CodCentroDefinitivo"]   = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["CodCentroCursoActual"]  = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Auxiliar"]              = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        
        self.posiciones_campos["IBAN"]      = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.posiciones_campos["Cuenta"]      = ProcesadorCSVGaseosa.CAMPO_NO_LOCALIZADO
        self.usar_nuevas_especialidades=False
        #Cargamos las especialidades
        self.especialidades=Especialidad.objects.all()

    #Determina las correspondencias entre las especialidades
    #antiguas (con 3 numeros) a las nuevas
    def set_activar_nuevas_especialidades(self, fichero_correspondencias):
        self.correspondencias=dict()
        with open(fichero_correspondencias, newline='', encoding="utf-8") as fichero_csv:
            lector=csv.reader(fichero_csv, delimiter=";", quotechar="\"")
            
            num_fila=0
            for fila in lector:
                if num_fila!=0:
                    self.correspondencias[fila[0]]=fila[1]
                num_fila=num_fila+1
        #print(self.correspondencias)
        self.usar_nuevas_especialidades=True
    
    #Si nos pasan la primera fila del CSV se rellenan las posiciones
    #de los campos
    def averiguar_posiciones_campos(self, lista_campos):
        pos_campo=0
        for campo in lista_campos:
            campo_sin_comillas=campo.replace("\"", "")
            for clave in self.posiciones_campos.keys():
                if clave==campo_sin_comillas:
                    self.posiciones_campos[clave]=pos_campo
            pos_campo+=1
        return self.posiciones_campos
    
    def reformatear_fecha(self, fecha):
        if fecha=="":
            fecha="01-01-1980"
        dia_nacimiento=fecha[0:2]
        mes_nacimiento=fecha[3:5]
        anio_nacimiento=fecha[6:10]
        return "-".join([anio_nacimiento, mes_nacimiento, dia_nacimiento])
        
        
    def get_especialidad(self, codigo_especialidad):
        #Las especialidad aqui son las de gaseosa, hay que pasarlas
        #al formato JCCM 0590xxx
        try:
            codigo_real=self.correspondencias[codigo_especialidad]            
            for e in self.especialidades:
                if e.codigo_especialidad==codigo_real:
                    #print (codigo_real)
                    return e
        except:
            print ("No se encontro la correspondencia de la especialidad -{0}".format(codigo_especialidad))
            return self.especialidades[0]
        return self.especialidades[0]
    
    def get_centro (self, cod_centro):
        
        cod_centro=cod_centro+"C"
        try:
            centro=Centro.objects.get(codigo_centro=cod_centro)
            return centro
        except:
            print ("No se encontro el centro:"+cod_centro)
            centro=Centro.objects.get(codigo_centro="9999"+"C")
            return centro
    def insertar_tuplas(self, tuplas):
        with transaction.atomic():
            for tupla in tuplas:
                #A los codigos de centro les añadimos la C
                #print("Buscando codigo:"+tupla[18])
                centro_def      =self.get_centro(tupla[18])
                #print("Buscando codigo:"+tupla[19])
                centro_actual   =self.get_centro(tupla[19])
                espe_asociada=self.get_especialidad(tupla[17])
                f_nacim=self.reformatear_fecha(tupla[10])
                #print (f_nacim)
                f_alta=self.reformatear_fecha(tupla[14])
                #print (f_alta)
                #No incluimos la fecha de baja
                g=Gaseosa(
                    dni=tupla[0], apellido_1=tupla[1], apellido_2=tupla[2],
                    nombre=tupla[3], sexo=tupla[4], direccion=tupla[5],
                    codigo_postal=tupla[6], especialidad=espe_asociada,
                    ciudad=tupla[7],provincia=tupla[8], email=tupla[9],
                    fecha_nacimiento=f_nacim, cuota=tupla[11],
                    tlf_casa=tupla[12], tlf_movil=tupla[13],
                    fecha_alta=f_alta, #fecha_baja=f_baja,
                    cuerpo=tupla[16],
                    cod_centro_def=centro_def,cod_centro_actual=centro_actual,
                    auxiliar=tupla[20], iban=tupla[21], ccc=tupla[22]
                )
                g.save()
            
    def insertar_en_bd(self, fichero_datos):
        tuplas=[]
        with open(fichero_datos, newline='', encoding="utf-8") as fichero_csv:
            lector=csv.reader(fichero_csv, delimiter=";", quotechar="\"")
            num_fila=0
            for fila in lector:
                if num_fila!=0:
                    for clave in self.posiciones_campos.keys():
                        nombre_campo=ProcesadorCSVGaseosa.CORRESPONDENCIA[clave]
                        pos_valor_campo=self.posiciones_campos[clave]
                        valor_campo=fila[pos_valor_campo]
                        #El campo fecha tiene que reordenarse de 31-11-2015 a 2015-11-31
                        if clave=="F_nace" or clave=="F_Alta" or clave=="F_Baja":
                            valor_campo=self.reformatear_fecha(valor_campo)
                        if clave=="Espec 1" and self.usar_nuevas_especialidades:
                            try:
                                valor_campo=self.correspondencias[valor_campo]
                            except KeyError:
                                valor_campo="101"
                    #Fin del for
                    tuplas.append (
                        (
                                fila[self.posiciones_campos["DNI"]],        #campo 0
                                fila[self.posiciones_campos["APELLIDO 1"]], #campo 1
                                fila[self.posiciones_campos["APELLIDO 2"]], #campo 2
                                fila[self.posiciones_campos["NOMBRE"]],     #campo 3
                                fila[self.posiciones_campos["SEXO"]],
                                fila[self.posiciones_campos["Dirección"]],
                                fila[self.posiciones_campos["C_Postal"]],
                                fila[self.posiciones_campos["Ciudad"]],
                                fila[self.posiciones_campos["Provincia"]],
                                fila[self.posiciones_campos["Email"]],
                                fila[self.posiciones_campos["F_nace"]],
                                fila[self.posiciones_campos["Cuota"]],
                                fila[self.posiciones_campos["Tfno_Casa"]  ],
                                fila[self.posiciones_campos["Tfno_Móvil"] ],
                                fila[self.posiciones_campos["F_Alta"]     ],
                                fila[self.posiciones_campos["F_Baja"]     ],
                                fila[self.posiciones_campos["Cuerpo"]     ],
                                fila[self.posiciones_campos["Espec 1"]     ],                                
                                fila[self.posiciones_campos["CodCentroDefinitivo"]   ],
                                fila[self.posiciones_campos["CodCentroCursoActual"]  ],
                                fila[self.posiciones_campos["Auxiliar"]              ],                                
                                fila[self.posiciones_campos["IBAN"]      ],
                                fila[self.posiciones_campos["Cuenta"]]
                        )
                    )
                    
                else:
                    posiciones_campos=self.averiguar_posiciones_campos(fila)
                    #print (posiciones_campos)
                    #sys.exit(-1)
                num_fila+=1
            #print (tuplas)
            self.insertar_tuplas(tuplas)
        #Fin del with
