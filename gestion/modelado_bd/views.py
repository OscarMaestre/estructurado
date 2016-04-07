from django.shortcuts import render
from django.forms import modelformset_factory
from django.db.models import Q
# Create your views here.
from modelado_bd.models import InscripcionJornadas

import django_excel as excel #sudo pip3 install django-excel
import pyexcel.ext.xls  #sudo pip3 install pyexcel-xls


def get_inscripciones():
    no_ignorar=Q(pago="Efectivo") | Q(pago="Transferencia") | Q(pago="No pagado")
    inscripciones=InscripcionJornadas.objects.filter(no_ignorar).order_by("apellido1", "apellido2")
    return inscripciones
def datos_inscripciones ( peticion ):
    
    FormularioConjunto=modelformset_factory(InscripcionJornadas, exclude=("id_inscripcion", ))
    if peticion.method=="POST":
        formulario_masivo=FormularioConjunto(peticion.POST)
        if formulario_masivo.is_valid():
            formulario_masivo.save()
            contexto={
                "mensaje":"Los datos han sido almacenados"
            }
            return render(peticion, "modelado_bd/almacenado.html", contexto)
        else:
            contexto={
                "mensaje":"Los datos no han sido almacenados"
            }
            return render(peticion, "modelado_bd/almacenado.html")
    else:
        no_ignorar=Q(pago="Por procesar")
        formulario=FormularioConjunto(queryset=InscripcionJornadas.objects.filter(no_ignorar))
        contexto={
            "titulo":"Datos inscripciones",
            "formulario":formulario
        }
        return render(peticion, "modelado_bd/datos.html", contexto)
    
    
def listado_alfabetico(peticion):
    pagadas=Q(pago="Efectivo") | Q(pago="Transferencia")
    inscripciones=InscripcionJornadas.objects.filter(pagadas)
    lista=[]
    lista.append(
            ("Apellido1", "Apellido 2", "Nombre")
        )
    for i in inscripciones:
        if i.confirmada==True:
            confirmada="SI"
        else:
            confirmada="NO"
        lista.append(
            (i.apellido1, i.apellido2, i.nombre)
        )
    return excel.make_response_from_array(lista, 'xls', file_name="ListadoAlumnos.xls")
    

def index(peticion):
    inscripciones=get_inscripciones()
    pagadas_en_efectivo=InscripcionJornadas.objects.filter(pago="Efectivo").count()
    pagadas_por_transferencia=InscripcionJornadas.objects.filter(pago="Transferencia").count()
    total_pagadas=pagadas_en_efectivo + pagadas_por_transferencia
    total_inscripciones=len(inscripciones)
    total_sin_pagar=total_inscripciones - total_pagadas
    contexto={
        "inscripciones":inscripciones,
        "cantidad":len(inscripciones),
        "en_efectivo":pagadas_en_efectivo,
        "por_transferencia":pagadas_por_transferencia,
        "total_pagadas":total_pagadas,
        "total_sin_pagar":total_sin_pagar
    }
    return render(peticion, "modelado_bd/index.html", contexto)

def get_excel_inscripciones(peticion):
    inscripciones=get_inscripciones()
    lista=[]
    lista.append(
            ("NIF", "Apellido1", "Apellido 2", "Nombre","Especialidad",
             "Afiliado", "Años exp.", "Email", "Telefono", "Forma pago",
             "Confirma asist")
        )
    for i in inscripciones:
        if i.confirmada==True:
            confirmada="SI"
        else:
            confirmada="NO"
        lista.append(
            (i.nif, i.apellido1, i.apellido2, i.nombre,i.especialidad,
             i.afiliado, i.anios_exp, i.email, i.telefono,i.pago,
             confirmada)
        )
    return excel.make_response_from_array(lista, 'xls', file_name="InscripcionesJornadas.xls")