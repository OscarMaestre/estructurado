"""gestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from modelado_bd import views
from index import views as index_views
from django.conf import settings
from documentos import urls
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin_general"),
    url(r'^$', index_views.index),
    url(r'^datos/', views.datos_inscripciones, name="form_datos"),
    url(r'^inscripciones/', views.index, name="inscripciones"),
    url(r'^get_excel/', views.get_excel_inscripciones, name="get_excel"),
    url(r'^docs/', include ('documentos.urls'))
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print ("Patrones")
print (urlpatterns)
print ("Media ROOT:"+settings.MEDIA_ROOT)
print ("Media URL:"+settings.MEDIA_URL)
print (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


