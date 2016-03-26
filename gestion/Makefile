all:

clean:
	rm db.sqlite3; ./manage.py sqlflush; rm modelado_bd/migrations/*.py; touch modelado_bd/migrations/__init__.py ; ./manage.py makemigrations; ./manage.py migrate; ./manage.py createsuperuser --username usuario

ini:
	
	cd inicializacion/01_especialidades && ./crear_especialidades.py
	cd inicializacion/02_provincias && ./crear_provincias.py
	cd inicializacion/03_centros_localidades_y_zonas && ./dodo.py
	cd inicializacion/04_direc_postales_y_electronicas_centros && ./dodo.py
	cd inicializacion/30_etiquetas && ./dodo.py

nombramientos:
	cd asignaciones/20150828-todos-cuerpos && ./dodo.py
	cd asignaciones/20150908-todos-cuerpos && ./dodo.py
	cd asignaciones/AdjudicacionesResto20152016 && ./dodo.py
	cd tests && ./test_asignaciones.py