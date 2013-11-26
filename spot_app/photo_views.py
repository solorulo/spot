# -*- coding: utf-8 -*-
# Create your views here.
import os
from spot_app.models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.utils import simplejson

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.views.defaults import page_not_found

import math

# from django.contrib.gis.geos import *
# from django.contrib.gis.measure import D

# from django.views.decorators.csrf import csrf_exempt, wraps, available_attrs

import cloudinary
from cloudinary import uploader, utils, CloudinaryImage

def url(self, **options):
	options.update(format = self.format, version = self.version)
	return utils.cloudinary_url(self.public_id, **options)[0]

def photo_add(request):
	_json = {}
	try:
		if not request.user.is_authenticated():
			_json['status'] = {
				'code' : 401,
				'msg' : "Sesion no iniciada"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		if request.method == "GET" :
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo POST"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		foto_id = request.POST['id_image']
		desc = request.POST['desc']
		lat = request.POST['lat']
		lng = request.POST['lng']
		delay = request.POST['delay']
		urbex = request.POST['urbex']

		current_datetime = datetime.now()
		delayVal = current_datetime + datetime.timedelta(minutes = current_datetime)

		new_foto = Foto(
			foto_url=foto_id, 
			user=request.user, 
			fecha=current_datetime,
			delay=delayVal,
			descripcion=desc,
			urbex=urbex,
			latitud=lat,
			longitud=lng,
			xAccel=0,
			yAccel=0,
			zAccel=0)
		new_foto.save()
		_json['status'] = {
			'code' : 200,
			'msg' : "Bien"
		}

	except:
		_json['status'] = {
			'code' : 500,
			'msg' : "Internal Error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
