#!/usr/bin/env python3
#coding=utf-8

from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include (admin.site.urls)),
    url(r'^get_docs/(?P<ruta>[A-Z0-9/]+)/$', views.get_docs, name="get_docs"),
]
