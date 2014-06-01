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

def __init__(request):
	user_data = []
	try:
		
		if request.user.is_authenticated():

			# Agregamos mas campos al diccionario de informacion
			user_data['username'] = request.session['username']
			user_data['picture'] = request.session['picture']
			user_data['anonymous'] = request.session['anonymous']

			user_data['error'] = False # Agregamos la propiedad menu=True para mostrar el menu del usuario

		else:

			user_data['error'] = True
	
	except:

		session_key = request.session.session_key  # Sacamos el id de las variables de session

		session = Session.objects.get(session_key=session_key)
		uid = session.get_decoded().get('_auth_user_id')
		usu = User.objects.get(pk=uid) # Nos traemos el id yy el apodo del usuario
		
		informacion_usuario = Info_User.objects.get(user=usu.id) # Nos traemos toda la informacion personal del usuario
						
		# Almacenamos toda la informacion del usuario en variables de sesion para despues utilizarlas
		request.session['username'] = usu.username
		request.session['user_picture'] = url(informacion_usuario.picture)
		request.session['id'] = usu.id
		request.session['anonymous'] = informacion_usuario.anonymous

		# Agregamos mas campos al diccionario de informacion
		user_data['id'] = request.session['id']
		user_data['username'] = request.session['username']
		user_data['picture'] = request.session['picture']
		user_data['anonymous'] = request.session['anonymous']

		user_data['error'] = False # Agregamos la propiedad menu=True para mostrar el menu del usuario
	return user_data



def verify_session(request):
	_json = {}
	if request.method != "GET" :
		_json['status'] = {
			'code' : 405,
			'msg' : "Solo GET"
		}
		data = simplejson.dumps(_json)
		return HttpResponse(data)

	try:
		data = {}
		username = request.GET['username']
		if not request.user.is_authenticated():
			_json['status'] = {
				'code' : 406,
				'msg' : "User not aunthenticated"
			}
		elif request.user.username != username:
			_json['status'] = {
				'code' : 409,
				'msg' : "The user aunthenticated is another than requested"
			}
		else: 
			_json['status'] = {
				'code' : 200,
				'msg' : "OK"
			}
	except:
		_json['status'] = {
			'code' : 500,
			'msg' : "Internal Error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def verify_user(request):
	_json = {}
	try:
		if request.method == "GET" :
			data = {}
			username = request.GET['username']
			email = request.GET['email']
			mMessage = ""
			mAvailable = False
			try:
				User.objects.get( username=username )
				data["nav_username"] = True
				mMessage = "El usuario ya existe. "
				mAvailable = False
			except User.DoesNotExist:
				mAvailable = True
			try:
				User.objects.get( email=email )
				mMessage = mMessage + "Ya esta registrado ese email"
				data["nav_email"] = True
				mAvailable = False
			except User.DoesNotExist:
				mAvailable = mAvailable and True

			if mAvailable :
				_json['status'] = {
					'code' : 200,
					'msg' : "El usuario no existe"
				}
			else:
				_json['status'] = {
					'code' : 401,
					'msg' : mMessage
				}
				_json["data"] = data
		else:
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo GET"
			}
	except:
		_json['status'] = {
			'code' : 500,
			'msg' : "Internal Error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def profile(request):
	_json = {}
	try:
		if request.user.is_authenticated():
			if request.method == "GET" :
				data = {}
				user_id = request.GET['user_id']
				info_us = Info_User.objects.get(user_id=int(user_id))
				user = User.objects.get(pk=int(user_id))
				data['username'] = user.username
				likes = Like.objects.filter(user_id=int(user_id))
				data['likes']=likes.count()

				fotos = Photo.objects.filter(user_id=int(user_id))
				crews = Crew.objects.filter(owner=int(user_id))

				_jsoncrews = []
				for crew in crews:
					_jsoncrews.append({
						"nombre":crew.name,
						"id":crew.crew_id,
						"foto_url":url(crew.picture)
						})

				_jsonfotos = []
				for foto in fotos:
					_jsonfotos.append({
						"url":url(foto.picture),
						"id_foto":foto.pk
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

def register_image(request):
	_json = {}
	try:
		if not request.user.is_authenticated():
			_json['status'] = {
				'code' : 401,
				'msg' : "Sesion no iniciada"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		if request.method != "GET" :
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo GET"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		image_url = request.GET['id_image']

		if not image_url:
			_json['status'] = {
				'code' : 400,
				'msg' : "Dato inválido"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		user_id = request.user.pk
		info_us = Info_User.objects.get(user_id=int(user_id))
		info_us.picture = image_url
		info_us.save()

		_json['status'] = {
			'code' : 201,
			'msg' : "Bien"
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
		if (request.method != "POST"):
			_json['status'] = {
				'code' : 405,
				'msg' : "Solo POST"
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)

		errors = []	
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		# foto_url = request.POST['foto_url']
		
		# request.POST.get('anonimo','')
		if not username:
			errors.append("Introduce un nombre de usuario")
		if not password:
			errors.append("Introduce tu password")
		if not email and '@' not in email:
			errors.append("Introduce un email valido")

		if not errors:
			#verificar
			mMessage = ""
			mAvailable = False
			data = {}

			try:
				User.objects.get( username=username )
				data["nav_username"] = True
				mMessage = "El usuario ya existe. "
				mAvailable = False
			except User.DoesNotExist:
				mAvailable = True
			try:
				User.objects.get( email=email )
				mMessage = mMessage + "Ya esta registrado ese email"
				data["nav_email"] = True
				mAvailable = False
			except User.DoesNotExist:
				mAvailable = mAvailable and True

			if mAvailable :
				user = User.objects.create_user(username=username, email=email, password=password)
				user.save()
				info_user = Info_Usuario(user=user, anonimo=False )
				info_user.save()
				user = authenticate(username=username, password=password)
				auth_login(request, user)
				_json['status'] = {
					'code' : 201,
					'msg' : "Registro Creado, sesión iniciada"
				}
			else:
				_json['status'] = {
					'code' : 401,
					'msg' : mMessage
				}
				_json["data"] = data
		else:
			_json['status'] = {
				'code' : 401,
				'msg' : "Error"
			}
			_json['data'] = {
				'errors':errors
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
						'msg' : "Logged in "+user.username
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
