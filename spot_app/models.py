from django.db import models
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import *

# Create your models here. su mamada de no tocar de

class Crew(models.Model):
	nombre = models.CharField(max_length=30)
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	
	def __unicode__(self):
		return self.nombre

class Info_Usuario(models.Model):
	user = models.OneToOneField(User)
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	anonimo = models.BooleanField()
	crews = models.ManyToManyField(Crew)
	seguir = models.ManyToManyField("self")

	def __unicode__(self):
		return self.nombre

class Spot(models.Model):
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	latitud = models.DecimalField(decimal_places=7, max_digits=10)
	altitud = models.DecimalField(decimal_places=7, max_digits=10)
	likes = models.ManyToManyField(Info_Usuario)

class Foto(models.Model):
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	user = models.ForeignKey(User)
	spot = models.ForeignKey(Spot)
	fecha = models.DateTimeField()
	delay = models.DateTimeField()
	descripcion = models.CharField(max_length=250)
	crews = models.ManyToManyField(Crew)
	urbex = models.BooleanField()
	latitud = models.DecimalField(decimal_places=7, max_digits=10)
	altitud = models.DecimalField(decimal_places=7, max_digits=10)
	colonia = models.CharField(max_length=100)
	xAccel = models.DecimalField(decimal_places=7, max_digits=10)
	yAccel = models.DecimalField(decimal_places=7, max_digits=10)
	zAccel = models.DecimalField(decimal_places=7, max_digits=10)
	likes = models.ManyToManyField(Info_Usuario)
	
	def __unicode__(self):
		return self.descripcion

class Comentario(models.Model):
	texto = models.CharField(max_length=30)
	user = models.ForeignKey(User)
	foto = models.ForeignKey(Foto)
	
	def __unicode__(self):
		return self.nombre

class Ruta(models.Model):
	nombre = models.CharField(max_length=30)
	spots = models.ManyToManyField(Spot, through='Orden')
	likes = models.ManyToManyField(Info_Usuario)

	def __unicode__(self):
		return self.nombre

class Orden(models.Model):
	ruta = models.ForeignKey(Ruta)
	spot = models.ForeignKey(Spot)
	position = models.IntegerField()

