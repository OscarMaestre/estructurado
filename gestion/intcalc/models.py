from django.db import models

# Create your models here.


class Provincia(models.Model):
    codigo=models.CharField(max_length=4, primary_key=True)
    nombre=models.CharField(max_length=15)
    
    

class InterinoMaestroDisponible(models.Model):
    dni             =   models.CharField(max_length=12, primary_key=True)
    nombre_completo =   models.CharField(max_length=60)
    tipo_bolsa      =   models.CharField(max_length=10)
    orden_bolsa     =   models.IntegerField()
    provincia       =   models.ManyToManyField(Provincia)
