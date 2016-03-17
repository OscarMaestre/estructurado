#!/usr/bin/env python3
#coding=utf-8

from os import sep
URL_BASE="http://www.educa.jccm.es/educacion/cm/educa_jccm/BBDD_ACCESS.1.1.tkContent.27265/tkListResults?formName=SQLQueriesSearcher&nshow.sqlResults=3&position.sqlResults={0}&idQuery=961"
SUBDIRECTORIO_HTML="html_centros"
FICHERO_BASE=SUBDIRECTORIO_HTML + sep + "Centros{0}.html"
TOTAL_PAGINAS=583
NOMBRE_FICHERO_INFORMACION_CENTRO = SUBDIRECTORIO_HTML + sep + "Informacion-Centro-{0}.html"
URL_JUNTA="http://www.educa.jccm.es/"