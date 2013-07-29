from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db import models
import cloudinary
from cloudinary.models import *

class Info_Usuario(models.Model):

	user = models.OneToOneField(User, primary_key=True)
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	anonimo = models.BooleanField(default=False)

	seguir = models.ManyToManyField("self",null=True,blank=True)

	def __unicode__(self):
		return self.user.username

class Crew(models.Model):
	nombre = models.CharField(max_length=30)
	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	owner = models.ForeignKey(Info_Usuario, related_name='owner')
	members = models.ManyToManyField(Info_Usuario, related_name='members',null=True,blank=True)
	
	def __unicode__(self):
		return self.nombre

class Spot(models.Model):
	foto_url = CloudinaryField('foto_url',null=True,blank=True)

	latitud = models.DecimalField(decimal_places=7, max_digits=10)
	longitud = models.DecimalField(decimal_places=7, max_digits=10)
	# point = PointField()
	# objects = models.GeoManager()

	# likes = models.ManyToManyField(Like,null=True,blank=True)

class Etiqueta(models.Model):
	nombre = models.CharField(max_length=150, unique=True)
	def __unicode__(self):
		return self.nombre

class Foto(models.Model):

	foto_url = CloudinaryField('foto_url',null=True,blank=True)
	user = models.ForeignKey(Info_Usuario, blank=True, null=True)

	anonimo = models.BooleanField(default=False)
	spot = models.ForeignKey(Spot, blank=True, null=True)
	fecha = models.DateTimeField()
	delay = models.DateTimeField(blank=True, null=True)
	descripcion = models.CharField(max_length=250)
	urbex = models.BooleanField()

	latitud = models.DecimalField(decimal_places=7, max_digits=10)
	longitud = models.DecimalField(decimal_places=7, max_digits=10)
	# point = PointField()
	# objects = models.GeoManager()

	colonia = models.CharField(max_length=100)
	xAccel = models.DecimalField(decimal_places=7, max_digits=10)
	yAccel = models.DecimalField(decimal_places=7, max_digits=10)
	zAccel = models.DecimalField(decimal_places=7, max_digits=10)
	tags = models.ManyToManyField(Etiqueta,null=True,blank=True)
	
	def __unicode__(self):
		return self.descripcion

class Like(models.Model):
	user = models.ForeignKey(Info_Usuario)
	foto = models.ForeignKey(Foto)
	fecha = models.DateTimeField()

class Comparte (models.Model):
	user = models.ForeignKey(Info_Usuario)
	foto = models.ForeignKey(Foto)
	fecha = models.DateTimeField()

class Comentario(models.Model):
	texto = models.CharField(max_length=30)
	user = models.ForeignKey(Info_Usuario)
	foto = models.ForeignKey(Foto)
	fecha = models.DateTimeField()
	
	
	def __unicode__(self):
		return self.nombre

class Ruta(models.Model):
	nombre = models.CharField(max_length=30)
	spots = models.ManyToManyField(Spot, through='Orden')
	# likes = models.ManyToManyField(Like,null=True,blank=True)

	# objects = models.GeoManager()

	def __unicode__(self):
		return self.nombre

class Orden(models.Model):
	ruta = models.ForeignKey(Ruta)
	spot = models.ForeignKey(Spot)
	position = models.IntegerField()

