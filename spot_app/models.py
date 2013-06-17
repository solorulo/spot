from django.db import models
from django.contrib.auth.models import User

# Create your models here. su mamada de no tocar de

class Crew(models.Model):
	nombre = models.CharField(max_length=30)
	foto_url = models.CharField(max_length=60)
	
	def __unicode__(self):
		return self.nombre

class Info_Usuario(models.Model):
	user = models.OneToOneField(User)
	foto_url = models.CharField(max_length=60)
	anonimo = models.BooleanField()
	crews = models.ManyToManyField(Crew)
	seguir = models.ManyToManyField("self")

	def __unicode__(self):
		return self.nombre

class Spot(models.Model):
	foto_url = models.CharField(max_length=60)
	latitud = models.DecimalField(decimal_places=7, max_digits=10)
	altitud = models.DecimalField(decimal_places=7, max_digits=10)
	likes = models.ManyToManyField(Info_Usuario)
	
	def __unicode__(self):
		return self.nombre

class Foto(models.Model):
	foto_url = models.CharField(max_length=60)
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
		return self.foto_url

class Comentario(models.Model):
	texto = models.CharField(max_length=30)
	user = models.ForeignKey(User)
	foto = models.ForeignKey(Foto)
	
	def __unicode__(self):
		return self.nombre

class Ruta(models.Model):
	nombre = models.CharField(max_length=30)
	spots = models.ManyToManyField(Spot)
	likes = models.ManyToManyField(Info_Usuario)

	def __unicode__(self):
		return self.nombre
