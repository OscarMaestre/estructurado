from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from modelado_bd import models as modelos_db
# Create your models here.

class ResultadoConcurso(models.Model):
    RESULTADO=[
        ("DENEGADO", "DENEGADO"),
        ("OBTIENE PLAZA", "OBTIENE PLAZA"),
        ("PEND. DESTINO", "PENDIENTE DESTINO")
    ]
    dni                 = models.CharField(
        primary_key=True, max_length=10, db_index=True)
    nombre_completo     = models.CharField( max_length=80 )
    centro_anterior     = models.ForeignKey (
        modelos_db.Centro, blank=True, related_name="concurso_centro_ant" )
    centro_definitivo   =models.ForeignKey (
        modelos_db.Centro, blank=True, related_name="concurso_centro_def")
    resultado           = models.CharField ( max_length=40, choices=RESULTADO )
    class Meta:
        db_table = 'resultados_concurso'
        #ordering=['apellido_1', 'apellido_2', 'nombre']
        
@receiver ( pre_save, sender=ResultadoConcurso )

def determinar_resultado ( sender, **argumentos ):
    instancia=argumentos["instance"]
    if instancia.centro_definitivo!=None:
        instancia.resultado="OBTIENE PLAZA"
        return
    if instancia.centro_definitivo==None:
        if instancia.centro_anterior==None:
            instancia.resultado="PEND. DESTINO"
        else:
            instancia.resultado="DENEGADO"
        return
    