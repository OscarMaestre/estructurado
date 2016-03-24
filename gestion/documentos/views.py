from django.shortcuts import render
from .models import Etiqueta, Fichero

from django.conf import settings

# Create your views here.

def index(peticion):
    etiquetas=Etiqueta.objects.all().order_by("valor")
    contexto={
        "etiquetas":etiquetas
    }
    return render (peticion, "documentos/index.html", contexto)

def get_docs(peticion, ruta):
    textos=ruta.split("/")
    
    ficheros=Fichero.objects.filter(etiquetas__in=textos).order_by("archivo").distinct()
    cantidad=len(ficheros)
    contexto={
        "ficheros":ficheros,
        "url_base":settings.MEDIA_URL,
        "cantidad":cantidad
    }
    return render (peticion, "documentos/resultados.html", contexto)