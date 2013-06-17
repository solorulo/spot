from django.db import models

# Create your models here.
class Usuario(models.Model):
	nombre = models.CharField(max_length=30)
	usuario = models.CharField(max_length=30)
	mail = models.EmailField(max_length=30)
	password = models.CharField(max_length=30)
	foto_url = models.CharField(max_length=30)
	anonimo = models.BooleanField()

	def __unicode__(self):
		return self.nombre

class Foto(models.Model):
	nombre = models.CharField(max_length=30)
	usuario = models.ForeignKey(Usuario)
	descripcion = models.CharField(max_length=30)
	fecha = models.DateTimeField(auto_now=True, auto_now_add=False)
	delay = models.DateTimeField(auto_now=False)
	urbex = models.BooleanField()
	url = models.CharField(max_length=60)
	xAccel = models.DecimalField(max_digits=5, decimal_places=10)
	yAccel = models.DecimalField(max_digits=5, decimal_places=10)
	zAccel = models.DecimalField(max_digits=5, decimal_places=10)
	latitud = models.DecimalField(max_digits=9, decimal_places=18)
	altitud = models.DecimalField(max_digits=9, decimal_places=18)
	
	def __unicode__(self):
		return self.nombre

class Spot(models.Model):
	nombre = models.CharField(max_length=30)
	latitud = models.DecimalField(max_digits=9, decimal_places=18)
	altitud = models.DecimalField(max_digits=9, decimal_places=18)
	img_url = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.nombre

class Crew(models.Model):
	nombre = models.CharField(max_length=30)
	#fotos many to manyhgte ghj9k0lñp
	d2w
	
	def __unicode__(self):
		return self.nombre

class Comentario(models.Model):
	texto = models.CharField(max_length=240)
	#foto