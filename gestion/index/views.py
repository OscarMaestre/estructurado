from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.admin import AdminSite, site

# Create your views here.

def index(peticion):
    sitio=site.each_context(peticion)
    contexto={
        "url_admin":sitio
    }
    return render (peticion, "index/base.html", contexto)
