#coding=utf-8
from __future__ import unicode_literals
import os
from django.db import models
from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utilidades.internet.internet import get_latitud_longitud
from utilidades.modelos.Modelos import get_directorio_archivos_especialidades,extraer_tuplas_especialidades_de_fichero
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
    
    def __str__(self ):
        return self.codigo_especialidad + " " + self.descripcion
    
    class Meta:
        db_table = 'especialidades'
        verbose_name_plural="especialidades"
        
    @staticmethod
    def crear_especialidad(codigo_cuerpo, crear_bolsas_asociadas=False):
        f=codigo_cuerpo
        sql=[]
        dir_datos=get_directorio_archivos_especialidades()
        ruta_fichero=dir_datos+os.path.sep+"Especialidades0{0}.txt".format(f)
        especialidades=extraer_tuplas_especialidades_de_fichero( ruta_fichero )
        lista_especialidades_a_insertar=[]
        for tupla in especialidades:
            codigo_especialidad_extraida=tupla[0]
            nombre=tupla[1]
            exige_bilingue_ingles=True
            no_exige_bilingue_ingles=False
            exige_bilingue_frances=True
            no_exige_bilingue_frances=False
            es_a_tiempo_parcial=True
            no_es_a_tiempo_parcial=False
            #Creamos todas las especialidades con todas las combinaciones
            #de ingles y frances
            
            #0590107 es 0(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="0"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_ESPANOL,
                tipo_de_jornada=Especialidad.JORNADA_COMPLETA
            )
            especialidad.save()
            #P590107 es P(Tiempo completo, sin bilingüismo) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="P"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_ESPANOL,
                tipo_de_jornada=Especialidad.MEDIA_JORNADA
            )
            especialidad.save()
            
            #B590107 es B(Tiempo completo, bilingüe inglés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="B"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_INGLES,
                tipo_de_jornada=Especialidad.JORNADA_COMPLETA
            )
            especialidad.save()
            
            #W590107 es W(Tiempo parcial, bilingüe inglés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="W"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_INGLES,
                tipo_de_jornada=Especialidad.MEDIA_JORNADA
            )
            especialidad.save()
            
            #F590107 es F(Tiempo completo, bilingüe francés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="F"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_FRANCES,
                tipo_de_jornada=Especialidad.JORNADA_COMPLETA
            )
            especialidad.save()
            
            #R590107 es R(Tiempo parcial, bilingüe francés) 590 Secund 107 Informatica
            especialidad=Especialidad(
                codigo_especialidad="R"+codigo_cuerpo+codigo_especialidad_extraida,
                descripcion=nombre,
                idioma=Especialidad.IDIOMA_FRANCES,
                tipo_de_jornada=Especialidad.MEDIA_JORNADA
            )
            especialidad.save()
    
    @staticmethod
    def crear_todas_especialidades():
        with transaction.atomic():
            cuerpos=["590", "591", "592", "594", "595", "511","597", "596"]
            for cuerpo in cuerpos:
                Especialidad.crear_especialidad( cuerpo )

        
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
    CODIGOS_PROVINCIAS={
        "13":"CR",
        "45":"TO",
        "02":"AB",
        "06":"CU",
        "19":"GU"
    }
        
    provincia=models.CharField(max_length=4, primary_key=True, choices=PROVINCIAS)
    class Meta:
        db_table = 'provincias'
        
    def __str__(self):
        return self.provincia
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
    def __str__(self):
        return self.nombre_localidad
    
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

class Ruta(models.Model):
    origen      =   models.ForeignKey ( Localidad, related_name="loc_origen" , db_index=True)
    destino     =   models.ForeignKey ( Localidad, related_name="loc_destino", db_index=True)
    distancia   =   models.IntegerField()
    minutos     =   models.IntegerField()
    sumario     =   models.CharField ( max_length=250 )
    def __str__(self):
        cad="""
        {0}--{1}   {2} minutos, {3} km
        """
        return cad.format(
            self.origen,
            self.destino,
            self.distancia,
            self.minutos
        )
    class Meta:
        db_table="rutas"



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
    VACANTES_08_09_2015="Vacantes 08-09-2015"
    VACANTES_18_09_2015="Vacantes 18-09-2015"
    ASIGNACION_SUSTITUCIONES="Asignación de sustituciones de "
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
    confirmada      =   models.BooleanField(default=False)
    def  __str__(self):
        return "{0} {1}, {2} ({3}-{4})".format(
            self.apellido1, self.apellido2, self.nombre, self.id_inscripcion, self.pago)
    
    class Meta:
        db_table="inscripciones_jornadas"
        ordering=['apellido1', 'apellido2']
        
@receiver(pre_save, sender=InscripcionJornadas)
def corregir_nombre_localidad_cra(sender, **argumentos):
    inscripcion=argumentos["instance"]
    inscripcion.apellido1=inscripcion.apellido1.upper()
    inscripcion.apellido2=inscripcion.apellido2.upper()
    inscripcion.nombre=inscripcion.nombre.upper()
    
    
    
    
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
    cod_centro_def      = models.ForeignKey(Centro, related_name="centro_definitivo")
    cod_centro_actual   = models.ForeignKey(Centro, related_name="centro_actual")
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
     
    
class InterinoDisponible(models.Model):
    POSIBLES_BOLSAS=[
        ("0",   "Bolsa 0"),
        ("1",   "Bolsa 1"),
        
        ("2D",   "Bolsa 2D"),
        ("2F",   "Bolsa 2F"),
        ("2H",   "Bolsa 2H"),
        ("2J",   "Bolsa 2J"),
        ("2K",   "Bolsa 2K"),
        ("2L",   "Bolsa 2L"),
        ("2M",   "Bolsa 2M"),
        ("3H",   "Bolsa 3H"),
        ("3G",   "Bolsa 3G"),
        ("2",   "Bolsa 2"),
        ("3",   "Bolsa 3"),
        ("4F",   "Bolsa 4F"),
        ("4",   "Bolsa 4"),
        ("6M",   "Bolsa 6M"),
        ("6",   "Bolsa 6"),
        ("7G",  "Bolsa 7G"),
        ("7P",  "Bolsa 7P"),
        ("7J",   "Bolsa 7J"),
        ("8",   "Bolsa 8"),
        ("P0",  "Bolsa P0"),
        ("P1B",  "Bolsa P1B"),
        ("P1",  "Bolsa P1"),
        ("P2",  "Bolsa P2"),
        ("P4",  "Bolsa P4"),
        ("R1",  "Bolsa R1"),
        ("2N",  "Bolsa 2N"),
        ("4E",  "Bolsa 4E"),
        ("4G",  "Bolsa 4G"),
        ("R1H",  "Bolsa R1H"),
        ("R1F",  "Bolsa R1F"),
        ("R1D",  "Bolsa R1D"),
        ("R1G",  "Bolsa R1G"),
        ("R1I",  "Bolsa R1I"),
    ]
    orden           =   models.IntegerField()
    dni             =   models.CharField( max_length=12 )
    nombre_completo =   models.CharField ( max_length=100 )
    tipo_bolsa      =   models.CharField( max_length=10, choices=POSIBLES_BOLSAS )
    orden_bolsa     =   models.IntegerField()
    ingles          =   models.BooleanField()
    frances         =   models.BooleanField()
    especialidad    =   models.ManyToManyField ( Especialidad )
    
    elige_ab        =   models.BooleanField(default=False)
    elige_cr        =   models.BooleanField(default=False)
    elige_cu        =   models.BooleanField(default=False)
    elige_gu        =   models.BooleanField(default=False)
    elige_to        =   models.BooleanField(default=False)
    def __str__(self):
        return self.dni + " orden bolsa:" + str ( self.orden_bolsa )
    class Meta:
        db_table = 'interinos_disponibles'
        
    
    
class ProvinciaOpos2016(models.Model):
    codigo_provincia    =   models.CharField(max_length=15, primary_key=True, db_index=True)
    nombre_provincia    =   models.CharField(max_length=15)
    
class LocalidadOpos2016(models.Model):
    codigo_localidad    =   models.CharField(max_length=12, primary_key=True, db_index=True)
    nombre_localidad    =   models.CharField(max_length=80, blank=False)
    provincia           =   models.ForeignKey(ProvinciaOpos2016)
    def __str__(self):
        return self.nombre_localidad
    
    class Meta:
        db_table = 'localidades_opos_2016'

class RutaOpos2016(models.Model):
    origen      =   models.ForeignKey ( LocalidadOpos2016, related_name="loc_origen" , db_index=True)
    destino     =   models.ForeignKey ( LocalidadOpos2016, related_name="loc_destino", db_index=True)
    distancia   =   models.IntegerField()
    minutos     =   models.IntegerField()
    sumario     =   models.CharField ( max_length=250 )
    def __str__(self):
        cad="""
        {0}--{1}   {2} minutos, {3} km
        """
        return cad.format(
            self.origen,
            self.destino,
            self.distancia,
            self.minutos
        )
    class Meta:
        db_table="rutas_opos_2016"
        
class CentroOpos2016(models.Model):
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
    localidad           =   models.ForeignKey(LocalidadOpos2016)
    def __str__(self):
        return self.nombre_centro
    class Meta:
        db_table = 'centros_opos_2016'

@receiver(pre_save, sender=CentroOpos2016)
def set_tipo_centro(sender, **argumentos):
    centro=argumentos["instance"]
    centro.nombre_centro=corregir_vi ( centro.nombre_centro )

@receiver(pre_save, sender=LocalidadOpos2016)
def corregir_nombre_localidad(sender, **argumentos):
    instancia_pueblo=argumentos["instance"]
    nombre_localidad=instancia_pueblo.nombre_localidad
    instancia_pueblo.nombre_localidad=rectificar_nombre_localidad ( nombre_localidad )
    
    return 
