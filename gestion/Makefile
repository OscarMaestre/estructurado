all:

clean:
	rm db.sqlite3; ./manage.py sqlflush; rm modelado_bd/migrations/*.py; touch modelado_bd/migrations/__init__.py ; ./manage.py makemigrations; ./manage.py migrate

ini:
	
	cd inicializacion/01_especialidades && ./crear_especialidades.py
	cd inicializacion/02_provincias && ./crear_provincias.py
	cd inicializacion/03_centros_localidades_y_zonas && ./dodo.py
	cd inicializacion/04_direc_postales_y_electronicas_centros && ./dodo.py

