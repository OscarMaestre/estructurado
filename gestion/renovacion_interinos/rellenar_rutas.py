#!/usr/bin/env python3
#coding=utf-8


from utilidades.basedatos.Configurador import Configurador
from utilidades.basedatos.GestorBD import GestorBD
import sys
configurador=Configurador ( ".." )
configurador.activar_configuracion ( "gestion.settings" )
from modelado_bd.models import *
from django.db import transaction


def corregir_nombre_localidad(nombre):
    
    #El nombre de la localidad de origen puede tener muchos otros errores
    #como llevar el articulo delante. Lo corregimos con esta
    #funcion que esta en modelado_bd.models
    nombre=rectificar_nombre_localidad ( nombre )

    #Algunos nombres están mal directamente en los PDF de la Junta
    #print ("Buscando correcciones en "+nombre)
    if nombre=="Garciotun":
        return "Garciotum"
    if nombre=="Las Ventas Con Peña Aguilera":
        print ("Corregido ventas")
        return "Las Ventas con Peña Aguilera"
    return nombre


def get_ruta(nombre_loc_origen, nombre_loc_destino, gestor_bd):
    nombre_loc_destino=corregir_nombre_localidad ( nombre_loc_destino )
    nombre_loc_origen=corregir_nombre_localidad ( nombre_loc_origen )
    #print (nombre_loc_origen, nombre_loc_destino)
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
    raise Exception
    return (0,0)


Ruta.objects.all().delete()
gestor_bd=GestorBD(".."+os.sep+"opos_2016"+os.sep+"rutas.db")

contador_rutas=1
with transaction.atomic():
    localidades=Localidad.objects.all()
    for origen in localidades:
        #print(dir(origen))
        for destino in localidades:
            if origen.codigo_localidad==destino.codigo_localidad:
                continue
            (tiempo_minutos, distancia_km)=get_ruta(
                origen.nombre_localidad,
                destino.nombre_localidad,
                gestor_bd)
            r=Ruta(
                
                minutos=tiempo_minutos,
                distancia=distancia_km
            )
            r.origen_id=origen.codigo_localidad
            r.destino_id=destino.codigo_localidad
            print (contador_rutas, r)
            contador_rutas+=1
            r.save()