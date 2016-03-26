#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utilidades.internet.internet import get_latitud_longitud
# Create your models here.


class Especialidad(models.Model):
    IDIOMA_ESPANOL="ESPANOL"
    IDIOMA_FRANCES="FRANCES"
    IDIOMA_INGLES="INGLES"
    JORNADA_COMPLETA="COMPLETA"
    MEDIA_JORNADA="MEDIA JORNADA"
    TERCIO_DE_JORNADA="TERCIO DE JORNADA"
    JORNADAS=[
        (JORNADA_COMPLETA, "Jornada Completa"),
        (MEDIA_JORNADA, "Media jornada"),
        (TERCIO_DE_JORNADA, "Tercio de Jornada")
    ]
    POSIBLES_IDIOMAS=[
        (IDIOMA_ESPANOL, "Sin bilingüismo"),
        (IDIOMA_FRANCES, "Bilingüe francés"),
        (IDIOMA_INGLES, "Bilingüe inglés")
    ]
    codigo_especialidad = models.CharField( max_length=8,primary_key=True, db_index=True)  
    descripcion         = models.CharField( max_length=80, blank=False, null=False) 
    idioma              = models.CharField( max_length=15, blank=False, null=False)
    tipo_de_jornada     = models.CharField( max_length=40, choices = JORNADAS)

    class Meta:
        db_table = 'especialidades'
        
        
class Gaseosa(models.Model):
    dni                 = models.CharField(primary_key=True, max_length=10, db_index=True)
    cuota               = models.CharField(max_length=10, blank=True, null=True)
    apellido_1          = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    apellido_2          = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    nombre              = models.CharField(max_length=60, blank=True, null=True)
    sexo                = models.CharField(max_length=2, blank=True, null=True)
    direccion           = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal       = models.CharField(max_length=6, blank=True, null=True)
    ciudad              = models.CharField(max_length=100, blank=True, null=True)
    provincia           = models.CharField(max_length=20, blank=True, null=True)
    email               = models.CharField(max_length=100, blank=True, null=True)
    especialidad        = models.ForeignKey(Especialidad)
    fecha_nacimiento    = models.DateField(blank=True, null=True)
    tlf_casa            = models.CharField(max_length=18, blank=True, null=True)
    tlf_movil           = models.CharField(max_length=18, blank=True, null=True)
    fecha_alta          = models.DateField(blank=True, null=True)
    fecha_baja          = models.DateField(blank=True, null=True)
    cuerpo              = models.CharField(max_length=10, blank=True, null=True)
    cod_centro_def      = models.CharField(max_length=12, blank=True, null=True)
    cod_centro_actual   = models.CharField(max_length=12, blank=True, null=True, db_index=True)
    auxiliar            = models.TextField(max_length=2048, blank=True, null=True)
    iban                = models.CharField(max_length=4, blank=True, null=True)
    ccc                 = models.CharField(max_length=20, blank=True, null=True)
    
    def get_ambos_apellidos(self):
        return self.apellido_1 + " " + self.apellido_2
    
    def get_nombre_completo(self, nombre_al_final=True):
        if nombre_al_final:
            return "{0} {1}, {2}".format (self.apellido_1, self.apellido_2, self.nombre)
        else:
            return "{0} {1}, {2}".format (self.nombre, self.apellido_1, self.apellido_2)
        
    def __str__(self):
        return self.get_nombre_completo()
        pass
    
    class Meta:
        db_table = 'gaseosa'
        ordering=['apellido_1', 'apellido_2', 'nombre']
        
        
class GaseoWeb(models.Model):
    dni                 = models.CharField(primary_key=True, max_length=10, db_index=True)
    apellido_1          = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    apellido_2          = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    nombre              = models.CharField(max_length=60, blank=True, null=True)
    class Meta:
        db_table="web"
        
        
class Provincia(models.Model):
    PROVINCIAS=[
        ("CR", "Ciudad Real"),
        ("AB", "Albacete"),
        ("GU", "Guadalajara"),
        ("TO", "Toledo"),
        ("CU", "Cuenca")
    ]
    provincia=models.CharField(max_length=4, primary_key=True, choices=PROVINCIAS)
    class Meta:
        db_table = 'provincias'
        
    @staticmethod
    def get_codigo(nombre_provincia_pasado):
        for p in Provincia.PROVINCIAS:
            (codigo, nombre)=p
            #print ("Examinando {0} frente a {1}".format ( nombre_provincia_pasado, nombre))
            if nombre==nombre_provincia_pasado:
                return codigo
        return "XX"

class Zona(models.Model):
    ZONA_CLM="Zona CLM"
    codigo_zona=models.CharField(max_length=10, primary_key=True, db_index=True)
    @staticmethod
    def get_zona_clm():
        z=Zona(codigo_zona=Zona.ZONA_CLM)
        z.save()
        return z
    def __str__(self):
        return self.codigo_zona
    class Meta:
        db_table = 'zonas'
    
    

class Localidad(models.Model):
    codigo_localidad    =   models.CharField(max_length=12, primary_key=True, db_index=True)
    nombre_localidad    =   models.CharField(max_length=80, blank=False)
    provincia           =   models.ForeignKey(Provincia)
    latitud             =   models.DecimalField(max_digits=11, decimal_places=8, default=0.0)
    longitud            =   models.DecimalField(max_digits=11, decimal_places=8, default=0.0)
    zona                =   models.ForeignKey ( Zona , blank=True)
    class Meta:
        db_table = 'localidades'
     
     
def corregir_vi(nombre_localidad):
    temp=nombre_localidad
    temp=temp.replace("VI", "Vi")
    return temp

def corregir_articulo(pueblo):
    pueblo=pueblo.strip()
    articulos=[" (El)", " (La)", " (Los)", " (Las)"]
    corregido=["El", "La", "Los", "Las"]
    
    for pos in range(0, len(articulos)):
        if pueblo.find(articulos[pos])!=-1:
            pueblo=pueblo.replace(articulos[pos], "")
            pueblo=corregido[pos]+" " + pueblo
            return pueblo
    return pueblo

def quitar_pueblo_entre_parentesis(cadena):
    pos_parentesis=cadena.find("(")
    if pos_parentesis!=-1:
        return cadena[:pos_parentesis-1]
    return cadena


def rectificar_nombre_localidad (nombre_localidad):
    nombre_localidad=corregir_articulo(nombre_localidad)
    nombre_localidad=corregir_vi(nombre_localidad)
    nombre_localidad=quitar_pueblo_entre_parentesis(nombre_localidad)
    return nombre_localidad

@receiver(pre_save, sender=Localidad)
def corregir_nombre_localidad(sender, **argumentos):
    instancia_pueblo=argumentos["instance"]
    nombre_localidad=instancia_pueblo.nombre_localidad
    instancia_pueblo.nombre_localidad=rectificar_nombre_localidad ( nombre_localidad )
    if instancia_pueblo.latitud==0.0:
        (latitud, longitud) = get_latitud_longitud(
            instancia_pueblo.nombre_localidad
        )
        instancia_pueblo.latitud=latitud
        instancia_pueblo.longitud=longitud
    return 





class Centro(models.Model):
    TIPOS=[
        ("CEIP", "(CEIP) Colegio de primaria"),
        ("CEE", "(CEE) Centro de Educación Especial"),
        ("CRA", "(CRA) Centro Rural Agrupado"),
        #IESO debe aparecer antes que IES
        ("IESO", "(IESO) Instituto de ESO"),
        ("IES", "(IES) Instituto de Educación Secundaria"),
        ("CIPFPU", "(CIPFPU) Centro Integrado de FP"),
        ("Cifppu", "(CIPFPU) Centro Integrado de FP"),
        ("Ifp", "(IFP) Centro Integrado de FP"),
        ("CPM", "(CPM) Conservatorio Profesional de Música"),
        ("CPD", "(CPM) Conservatorio Profesional de Danza"),
        ("SES", "(SES) Sección de Educación Secundaria"),
        ("EA", "(EA) Escuela de Artes"),
        ("EOI", "(EOI) Escuela Oficial de Idiomas"),
        ("CEPA", "(CEPA) Centro Educación Personas Adultas"),
        ("AEPA", "(AEPA) Aul Educación Personas Adultas"),
        ("UO", "(UO) Unidad de Orientacion"),
        ("DP", "(DP) Delegación Provincial de Educación"),
        ("DESC", "(DESC) Desconocido")
    ]
    NATURALEZAS=[
        ("Público", "Público"),
        ("Privado", "Privado"),
        ("Concertado", "Concertado"),
        ("Desconocida", "Desconocida")
    ]
    codigo_centro       =   models.CharField(max_length=10, primary_key=True, db_index=True)
    nombre_centro       =   models.CharField(max_length=60)
    tipo_centro         =   models.CharField(max_length=12, choices=TIPOS)
    localidad           =   models.ForeignKey(Localidad)
    naturaleza          =   models.CharField(max_length=15, choices=NATURALEZAS, default="Público")
    class Meta:
        db_table = 'centros'

@receiver(pre_save, sender=Centro)
def set_tipo_centro(sender, **argumentos):
    centro=argumentos["instance"]
    
    #Muchos centros llevan incluido en el pueblo el nombre
    centro.nombre_centro=quitar_pueblo_entre_parentesis ( centro.nombre_centro )
    #En algunos pone VIllanueva (dos mayúsculas seguidas)
    centro.nombre_centro=corregir_vi ( centro.nombre_centro )
    #Algunos centros tienen mal el nombre de la EOI
    centro.nombre_centro=centro.nombre_centro.replace("Eeoi", "EOI")
    #Se averigua el tipo
    inicio_nombre=centro.nombre_centro[:6]
    for c in Centro.TIPOS:
        posible_tipo=c[0]
        if inicio_nombre.find(posible_tipo)!=-1:
            centro.tipo_centro=posible_tipo
            #print ("Tipo:"+centro.tipo_centro)
            return
    #Fin del for
    centro.tipo_centro="DESC"
    
    print ("El centro {0} tiene un tipo DESCONOCIDO".format(centro.nombre_centro))
    return 
    

class LocalidadAsociadaCRA(models.Model):
    nombre_localidad=models.CharField(max_length=50, blank=False, null=False)
    cra_cabecera=models.ForeignKey( Centro )
    
    class Meta:
        db_table="localidades_de_cra"

        
        
def corregir_latitud_longitud(instancia):
    (latitud_longitud)=get_latitud_longitud( nombre_localidad )
    return (latitud, longitud)

@receiver(pre_save, sender=LocalidadAsociadaCRA)
def corregir_nombre_localidad_cra(sender, **argumentos):
    instancia_pueblo=argumentos["instance"]
    nombre_localidad=instancia_pueblo.nombre_localidad
    nombre_localidad=corregir_vi(nombre_localidad)
    nombre_localidad=quitar_pueblo_entre_parentesis(nombre_localidad)
    nombre_localidad=corregir_articulo(nombre_localidad)
    instancia_pueblo.nombre_localidad=nombre_localidad
    return 




class DireccionesCentro(models.Model):
    centro              =   models.ForeignKey ( Centro )
    direccion_postal    =   models.CharField(max_length=120, blank=False)
    codigo_postal       =   models.CharField(max_length=6, blank=False)
    localidad           =   models.ForeignKey(Localidad)
    tlf                 =   models.CharField(max_length=15)
    fax                 =   models.CharField(max_length=15)
    email               =   models.CharField(max_length=160)
    web                 =   models.CharField(max_length=160)
    
    def __str__(self):
        return self.nombre_centro + " " + self.codigo_localidad
    
    class Meta:
        db_table="direcciones_centros"
        
        
class ProcedimientoAdjudicacion(models.Model):
    VACANTES_28_08_2015="Vacantes 28-08-2015"
    VACANTES_18_09_2015="Vacantes 18-09-2015"
    nombre      =   models.CharField(max_length=150, primary_key=True)
    fecha       =   models.DateField()
    class Meta:
        db_table="procedimientos_adjudicacion"
    
class Nombramiento(models.Model):
    nif             =   models.CharField(max_length=12)
    nombre_completo =   models.CharField(max_length=180)
    centro          =   models.ForeignKey ( Centro )
    fecha_inicio    =   models.DateField()
    fecha_fin       =   models.DateField()
    especialidad    =   models.ForeignKey ( Especialidad )
    proceso         =   models.ForeignKey ( ProcedimientoAdjudicacion )
    auxiliar        =   models.CharField ( max_length=240 )
    
    class Meta:
        db_table="nombramientos"
        
        

    
class InscripcionJornadas(models.Model):
    TIPOS_PAGO  = [
        ("Por procesar", "Por procesar"),
        ("Efectivo", "Pagado en efectivo"),
        ("Transferencia", "Pagado por transf"),
        ("No pagado", "No pagado"),
        ("Descartada", "Descartada")
    ]
    id_inscripcion  =   models.IntegerField(primary_key=True)
    nif             =   models.CharField(max_length=12, blank=True, null=True)
    apellido1       =   models.CharField(max_length=60)
    apellido2       =   models.CharField(max_length=60)
    nombre          =   models.CharField(max_length=80)
    email           =   models.EmailField()
    telefono        =   models.CharField(max_length=15)
    anios_exp       =   models.IntegerField()
    especialidad    =   models.CharField(max_length=30)
    afiliado        =   models.CharField(max_length=10)
    pago            =   models.CharField(max_length=20, choices=TIPOS_PAGO)
    def  __str__(self):
        return "{0} {1}, {2} ({3}-{4})".format(
            self.apellido1, self.apellido2, self.nombre, self.id_inscripcion, self.pago)
    
    class Meta:
        db_table="inscripciones_jornadas"
        
@receiver(pre_save, sender=InscripcionJornadas)
def corregir_nombre_localidad_cra(sender, **argumentos):
    inscripcion=argumentos["instance"]
    inscripcion.apellido1=inscripcion.apellido1.upper()
    inscripcion.apellido2=inscripcion.apellido2.upper()
    inscripcion.nombre=inscripcion.nombre.upper()