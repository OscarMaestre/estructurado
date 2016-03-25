CONVERSOR=pdftotext
FLAGS=-nopgbrk -layout

FICHERO_SQL_FINAL=asignacion_28-Ago-2015.sql

all: %.txt

%.txt : %.pdf
	$(CONVERSOR) $(FLAGS) $< > $@
clean:
	rm *.txt; rm *.sql
