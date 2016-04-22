#!/usr/bin/env python3
#coding=utf-8


from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
from django.db import transaction


def get_ruta(nombre_loc_origen, nombre_loc_destino, gestor_bd):
    sql_origen_destino="""
        select origen, destino, minutos, distancia
        from rutas
            where origen='{0}'
            and
                destino='{1}'
        
    """.format(nombre_loc_origen, nombre_loc_destino)  
    #print (sql)
    filas=gestor_bd.get_filas ( sql_origen_destino )
    if len(filas)!=0:
        fila=filas[0]
        minutos=fila[2]
        distancia=fila[3]
        return (minutos, distancia)
    #Si llegamos hasta aqui estamos probando la ruta inversa
    sql_destino_origen="""
        select origen, destino, minutos, distancia
        from rutas
            where destino='{0}'
            and
                origen='{1}'
        
    """.format(nombre_loc_origen, nombre_loc_destino)  
    #print (sql)
    filas=gestor_bd.get_filas ( sql_destino_origen )
    if len(filas)!=0:
        fila=filas[0]
        minutos=fila[2]
        distancia=fila[3]
        return (minutos, distancia)
    
    print(sql_origen_destino)
    print(sql_destino_origen)
    print (nombre_loc_origen+" no encontrada")
    print (nombre_loc_destino+" no encontrada")
    return (0,0)


RutaOpos2016.objects.all().delete()
gestor_bd=GestorBD("rutas.db")

contador_rutas=1
with transaction.atomic():
    localidades=LocalidadOpos2016.objects.all()
    for origen in localidades:
        #print(dir(origen))
        for destino in localidades:
            if origen.codigo_localidad==destino.codigo_localidad:
                continue
            (tiempo_minutos, distancia_km)=get_ruta(
                origen.nombre_localidad,
                destino.nombre_localidad,
                gestor_bd)
            r=RutaOpos2016(
                
                minutos=tiempo_minutos,
                distancia=distancia_km
            )
            r.origen_id=origen.codigo_localidad
            r.destino_id=destino.codigo_localidad
            print (contador_rutas, r)
            contador_rutas+=1
            r.save()