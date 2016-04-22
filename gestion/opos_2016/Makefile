FICH_CENTROS_PDF=centros.pdf
FICH_REGISTROS=registros.txt

all: traer_ruta actualizar cortar crear_rutas

actualizar:torre villafranca ventas


torre:
	echo "update rutas set origen='La Torre de Esteban Hambran' where origen='Torre de Esteban Hambran';" | sqlite3 rutas.db 
villafranca:
	echo "update rutas set origen='Villafranca de los Caballeros' where origen='Villafranca de los';" | sqlite3 rutas.db
ventas:
	echo "update rutas set origen='Las Ventas con Peña Aguilera' where origen='Ventas Con Peña Aguilera';" | sqlite3 rutas.db

traer_ruta:
	cp ~/repos/varios/pruebas_proceso/Verano/calculador-rutas-globales/rutas.db .
cortar:
	pdftk A=Convocatoria.pdf cat A77-120 output $(FICH_CENTROS_PDF); ./extraer_centros.py $(FICH_CENTROS_PDF) > $(FICH_REGISTROS)

crear_rutas:
	./rellenar_datos.py $(FICH_REGISTROS) 
