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

def profile(request):
	_json = {}
	try:
		if request.user.is_authenticated():
			if request.method == "GET" :
				data = {}
				user_id = request.GET['user_id']
				info_us = Info_Usuario.objects.get(user_id=int(user_id))
				user = User.objects.get(pk=int(user_id))
				data['username'] = user.username
				likes = Like.objects.filter(user_id=int(user_id))
				data['likes']=likes.count()

				fotos = Foto.objects.filter(user_id=int(user_id))
				crews = Crew.objects.filter(owner=int(user_id))

				_jsoncrews = []
				for crew in crews:
					_jsoncrews.append({
						"nombre":crew.nombre,
						"id":crew.crew_id,
						"foto_url":url(crew.foto_url)
						})

				_jsonfotos = []
				for foto in fotos:
					_jsonfotos.append({
						"url":url(foto.foto_url),
						"id_foto":foto.foto_id
						})

				_json['status'] = {
					'code' : 200,
					'msg' : "Bien"
				}
				_json['data'] = {
					'info' : data,
					'fotos': _jsonfotos,
					"crews": _jsoncrews
				}
			else:
				_json['status'] = {
					'code' : 405,
					'msg' : "Solo POST"
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

def register(request):
	_json = {}
	try:
		if (request.method == "POST"):
			errors = []
			username = request.POST['username']
			password = request.POST['password']
			email = request.POST['email']
			foto_url = request.POST['foto_url']
			
			# request.POST.get('anonimo','')
			if not username:
				errors.append("Introduce un nombre de usuario")
			if not password:
				errors.append("Introduce tu password")
			if not email and '@' not in email:
				errors.append("Introduce un email valido")

			if not errors:
				try:
					User.objects.get( username=username )
					_json['status'] = {
						'code' : 401,
						'msg' : "El usuario ya existe"
					}
				except User.DoesNotExist:
					# TODO registrar
					user = User.objects.create_user(username=username, email=email, password=password)
					user.save()
					info_user = Info_Usuario(user=user, foto_url=foto_url, anonimo=False )
					info_user.save()
					_json['status'] = {
						'code' : 201,
						'msg' : "Registro Creado"
					}
			else:
				_json['status'] = {
					'code' : 401,
					'msg' : "Error"
				}
				_json['data'] = {
					'errors':errors
				}
		else:
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo POST"
			}
	except:
		_json['status'] = {
			'code' : 401,
			'msg' : "Ha ocurrido un error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def login(request):
	_json = {}
	try:
		if (request.method == "POST"):
			errors = []
			username = request.POST['username']
			password = request.POST['password']
			
			# request.POST.get('anonimo','')
			if not username:
				errors.append("Introduce un nombre de usuario")
			if not password:
				errors.append("Introduce tu password")

			if not errors:
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
					# Correct password, and the user is marked "active"
					auth_login(request, user)
					# Redirect to a success page.
					_json['status'] = {
						'code' : 200,
						'msg' : "Logged in"
					}
				else:
					# Show an error page
					_json['status'] = {
						'code' : 401,
						'msg' : "Revisa tu contraseña"
					}
			else:
				_json['status'] = {
					'code' : 401,
					'msg' : "Error"
				}
				_json['data'] = {
					'errors':errors,
					'username':username,
					'password':password
				}
		else:
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo POST"
			}
	except:
		_json['status'] = {
			'code' : 401,
			'msg' : "Ha ocurrido un error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def logout(request):
	_json = {}
	try:
		auth_logout(request)
		_json['status'] = {
			'code' : 201,
			'msg' : "Ha salido de la aplicación exitosamente"
		}
	except:
		_json['status'] = {
			'code' : 401,
			'msg' : "Ha ocurrido un error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
