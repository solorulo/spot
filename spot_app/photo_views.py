# -*- coding: utf-8 -*-
# Create your views here.
import os
from spot_app.models import *
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

from django.contrib.gis.geos import *
from django.contrib.gis.measure import D

# from django.views.decorators.csrf import csrf_exempt, wraps, available_attrs

import cloudinary
from cloudinary import uploader, utils, CloudinaryImage

def handler404(request):
	_json = {}
	_json['status'] = {
		'code' : 404,
		'msg' : "Not Found"
	}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
def handler500(request):
	_json = {}
	_json['status'] = {
		'code' : 500,
		'msg' : "Internal Error"
	}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def url(self, **options):
	options.update(format = self.format, version = self.version)
	return utils.cloudinary_url(self.public_id, **options)[0]

def home_nearby(request):
	_json = {}
	try:
		if request.user.is_authenticated():
			if request.method = "GET" :
				places = []

				latitud = request.GET['latitud']
				longitud = request.GET['longitud']
				limit = request.GET['cantidad']
				offset = request.GET['inicio']

				ref_point = Point(latitud, altitud)
				all_fotos = Foto.objects.all()[offset:limit].distance(ref_point).order_by('distance')

				

				all_fotos = Foto.objects.filter()


				_json['status'] = {
					'code' : 500,
					'msg' : "Internal Error"
				}
				_json['data'] = {
					'fotos' : places
				}
			else:
				_json['status'] = {
					'code' : 405,
					'msg' : "Sesion no iniciada"
				}
		else:
			_json['status'] = {
				'code' : 401,
				'msg' : "Sesion no iniciada"
			}
	except:
		_json['status'] = {
			'code' : 500,
			'msg' : "Internal Error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
