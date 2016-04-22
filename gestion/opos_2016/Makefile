FICH_CENTROS_PDF=centros.pdf
FICH_REGISTROS=registros.txt

all: traer_ruta actualizar cortar crear_centros crear_rutas informes

actualizar:
	./corregir_nombres.py

traer_ruta:
	cp ~/repos/varios/pruebas_proceso/Verano/calculador-rutas-globales/rutas.db .
cortar:
	pdftk A=Convocatoria.pdf cat A77-120 output $(FICH_CENTROS_PDF); ./extraer_centros.py $(FICH_CENTROS_PDF) > $(FICH_REGISTROS)

crear_centros:
	./rellenar_centros_localidades.py $(FICH_REGISTROS)

crear_rutas:
	./rellenar_rutas.py

informes:
	rm informes/* ; ./generar_informes.py
