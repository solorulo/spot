import datetime
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db import models
import cloudinary
from cloudinary.models import *

class Info_User(models.Model):

	user = models.OneToOneField(User, primary_key=True)
	picture = CloudinaryField('picture',null=True,blank=True)
	anonymous = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username

class Spot(models.Model):
	name = models.CharField(max_length=280)
	picture = CloudinaryField('picture',null=True,blank=True)
	lat = models.DecimalField(decimal_places=7, max_digits=10, default=0.0)
	lng = models.DecimalField(decimal_places=7, max_digits=10, default=0.0)
	date_created=models.DateTimeField()

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date_created = datetime.datetime.today()
		return super(Spot, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Crew(models.Model):
	name = models.CharField(max_length=140)
	picture = CloudinaryField('picture',null=True,blank=True)
	owner = models.ForeignKey(User, related_name='owner')
	members = models.ManyToManyField(User, related_name='members',null=True,blank=True)
	
	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=140, unique=True)
	def __unicode__(self):
		return self.name

class Shareable(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=140)
	date_created=models.DateTimeField()

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['date_created']
		get_latest_by = 'date_created'

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date_created = datetime.datetime.today()
		return super(Shareable, self).save(*args, **kwargs)
			

class Photo(Shareable):
	spot = models.ForeignKey(Spot, blank=True, null=True)

	picture = CloudinaryField('picture',null=True,blank=True)
	description = models.CharField(max_length=280)

	anonymous = models.BooleanField(default=False)
	delay = models.DateTimeField(blank=True, null=True)
	urbex = models.BooleanField(default=False)

	lat = models.DecimalField(decimal_places=7, max_digits=10)
	lng = models.DecimalField(decimal_places=7, max_digits=10)
	# point = PointField()
	# objects = models.GeoManager()

	other = models.CharField(max_length=280,null=True,blank=True)
	xAccel = models.DecimalField(decimal_places=7, max_digits=10)
	yAccel = models.DecimalField(decimal_places=7, max_digits=10)
	zAccel = models.DecimalField(decimal_places=7, max_digits=10)
	tags = models.ManyToManyField(Tag,null=True,blank=True)
	
	def __unicode__(self):
		return self.description

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date_created = datetime.datetime.today()
		return super(Photo, self).save(*args, **kwargs)

class Like(models.Model):
	user = models.ForeignKey(User)
	photo = models.ForeignKey(Photo)
	date_created = models.DateTimeField()

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date_created = datetime.datetime.today()
		return super(Like, self).save(*args, **kwargs)

class Shared (models.Model):
	user = models.ForeignKey(User)
	data = models.ForeignKey(Shareable)
	date = models.DateTimeField()

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date = datetime.datetime.today()
		return super(Shared, self).save(*args, **kwargs)

class Comment(models.Model):
	text = models.CharField(max_length=140)
	user = models.ForeignKey(User)
	photo = models.ForeignKey(Photo)
	date_created = models.DateTimeField()
	
	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.date_created = datetime.datetime.today()
		return super(Spot, self).save(*args, **kwargs)

class Route(Shareable):
	spots = models.ManyToManyField(Spot, through='Order')
	# likes = models.ManyToManyField(Like,null=True,blank=True)

	# objects = models.GeoManager()

	def __unicode__(self):
		return self.nombre

class Order(models.Model):
	route = models.ForeignKey(Route)
	spot = models.ForeignKey(Spot)
	order = models.IntegerField(default=0)
	
	class Meta:
		unique_together = (("route", "spot"),)
