from django.db import models

# Create your models here.
from django.urls import reverse
from datetime import date
from django.db.models import  Avg,F

def banderas_directory_path(instance, filename):
    return 'Ban/'.format(instance.nombre, filename)

def escudo_directory_path(instance, filename):
    return 'Esc/'.format(instance.nombre, filename)

class Equipo(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100,null=False,blank=False)
    bandera = models.ImageField(
        upload_to=banderas_directory_path, null=True, blank=True)
    escudo = models.ImageField(
        upload_to=escudo_directory_path, null=True, blank=True)
    

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("Equipo_detail", kwargs={"pk": self.pk})


class SuplentesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(titular=False)


class JugadorManager(models.Manager):
    
    def promedio_edad(self):
        return self.annotate(edad_prom=date.today().year - F('fecha_nacimiento__year'))


      
class Jugador(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    fecha_nacimiento=models.DateField(null=True, blank=True)
    posicion=models.CharField(max_length=100)
    numero=models.IntegerField(null=True, blank=True)
    titular=models.BooleanField(default=False)
    equipo = models.ForeignKey(
        Equipo, related_name='jugadores', on_delete=models.CASCADE)

    objects=JugadorManager()
    suplentes= SuplentesManager()
    
    class Meta:
        verbose_name = ("Jugador")
        verbose_name_plural = ("Jugadores")

    def __str__(self):
        return '%d.%s %s ' % (self.numero, self.nombre, self.apellido)
    
    @property
    def edad(self)->int:
        return date.today().year - self.fecha_nacimiento.year

class Tecnico(models.Model):
    
    TECNICO = 'Técnico'
    ASISTENTE = 'Asistente'
    MEDICO = 'Médico'
    PREPARADOR = 'Preparador'
    
    ROL_CHOICES = [
        (TECNICO, 'Técnico'),
        (ASISTENTE, 'Asistente'),
        (MEDICO, 'Médico'),
        (PREPARADOR, 'Preparador'),
    ]
    
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad=models.CharField(max_length=100)
    rol = models.CharField(
        max_length=10,
        choices=ROL_CHOICES,
        default=ASISTENTE)
    equipo = models.ForeignKey(
        Equipo, related_name='tecnicos', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Cuerpo Tecnico")
        verbose_name_plural = ("Tecnicos")

    def __str__(self):
        return '%s %s (%s)' % (self.nombre, self.apellido, self.rol)

    @property
    def edad(self) -> int:
        return date.today().year - self.fecha_nacimiento.year