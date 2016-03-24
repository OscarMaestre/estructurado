from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import datetime
from django.conf import settings
from os import remove

# Create your models here.

class Etiqueta(models.Model):
    valor=models.CharField(max_length=60, primary_key=True)
    
    def __str__(self):
        return self.valor
    class Meta:
        db_table="etiquetas"
        ordering=["valor"]
        
class Fichero(models.Model):
    archivo=models.FileField()
    descripcion=models.TextField()
    fecha_subida=models.DateField(default=datetime.date.today)
    fecha_documento=models.DateField()
    fecha_publicacion=models.DateField()
    etiquetas=models.ManyToManyField(Etiqueta)
    def __str__(self):
        return self.archivo.name
    
@receiver(pre_save, sender=Fichero)
def corregir_nombre_fichero(sender, **argumentos):
    instancia=argumentos["instance"]
    instancia.archivo.name=instancia.archivo.name.replace("./", "")
    print("Corrigiendo a "+instancia.archivo.name)
    
@receiver(post_delete, sender=Fichero)
def borrar_fichero(sender, **argumentos):
    instancia=argumentos["instance"]
    remove ( settings.MEDIA_ROOT+instancia.archivo.name)
    
@receiver(pre_save, sender=Etiqueta)
def corregir_nombre_etiqueta(sender, **argumentos):
    instancia=argumentos["instance"]
    instancia.valor=instancia.valor.upper()
    instancia.valor=instancia.valor.replace(" ", "_")