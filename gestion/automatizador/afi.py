#!/usr/bin/env python3
#coding=utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from utilidades.ficheros.GestorFicheros import GestorFicheros
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import os
import zipfile
import sys

usuario=sys.argv[1]
clave=sys.argv[2]
profile = FirefoxProfile();

path =os.path.dirname(os.path.abspath ( __file__ ))
print ("Descargando en "+path)
profile.set_preference("browser.download.folderList", 2);
profile.set_preference("browser.download.dir", path);
profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream");
profile.set_preference("browser.download.manager.showWhenStarting", False);
profile.set_preference("browser.download.manager.focusWhenStarting", False);  
profile.set_preference("browser.download.useDownloadDir", True);
profile.set_preference("browser.helperApps.alwaysAsk.force", False);
profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
profile.set_preference("browser.download.manager.closeWhenDone", True);
profile.set_preference("browser.download.manager.showAlertOnComplete", False);
profile.set_preference("browser.download.manager.useWindow", False);
profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False);
profile.set_preference("pdfjs.disabled", True);

browser = webdriver.Firefox(profile) # Get local session of firefox
browser.get("https://anpesindicato.org/afiliacion/index.php/control") # Load page
assert "ANPE" in browser.title
elem = browser.find_element_by_name("username") # Find the query box
elem.send_keys( usuario )
elem = browser.find_element_by_name("password") # Find the query box
elem.send_keys( clave + Keys.RETURN)
time.sleep(5) # Let the page load, will be added to the API

elem_lista=browser.find_element_by_link_text("Lista")

elem_lista.click()
time.sleep(4)
elem_exportar=browser.find_element_by_name("btnExcel")

elem_exportar.click()
elem_exportar.click()

time.sleep(5) # Let the page load, will be added to the API

browser.close()
gf=GestorFicheros()
zip_ref = zipfile.ZipFile("Afiliados.zip", 'r')
zip_ref.extractall(path)
zip_ref.close()
gf.borrar_fichero ( "Afiliados.zip")