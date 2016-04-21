FICH_CENTROS_PDF=centros.pdf
FICH_REGISTROS=registros.txt

all: cortar

cortar:
	pdftk A=Convocatoria.pdf cat A77-120 output $(FICH_CENTROS_PDF); ./extraer_centros.py $(FICH_CENTROS_PDF) > $(FICH_REGISTROS)

