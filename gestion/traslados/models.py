from django.db import models
from modelado_bd import models as modelos_db
# Create your models here.

class ResultadoConcurso(models.Model):
    dni                 = models.CharField(
        primary_key=True, max_length=10, db_index=True)
    centro_anterior     = models.ForeignKey (
        modelos_db.Centro, blank=True, related_name="concurso_centro_ant" )
    centro_definitivo   =models.ForeignKey (
        modelos_db.Centro, blank=True, related_name="concurso_centro_def")
    
    class Meta:
        db_table = 'resultados_concurso'
        #ordering=['apellido_1', 'apellido_2', 'nombre']