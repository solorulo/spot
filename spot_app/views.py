# -*- coding: utf-8 -*-
# Create your views here.
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.utils import simplejson

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def home(request):
	# user = User.objects.create_user( "rulo1", "email", "rulo" ) # Guardamos el usuario
	# user.is_staff = True
	# user.is_superuser = True
	# user.save()
	return render_to_response('home/home.html')

def register(request):
	_json = {}
	if (request.method == "POST"):
		errors = []
		username = request.POST.get('username','')
		name = request.POST.get('name','')
		password = request.POST.get('password','')
		email = request.POST.get('email','')
		foto_url = request.POST.get('foto_url','')
		anonimo = False # request.POST.get('anonimo','')
		if not username:
			errors.append("Introduce un nombre de usuario")
		if not name:
			errors.append("Introduce tu nombre")
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
				data = simplejson.dumps(_json)
				return HttpResponse(data)
			except User.DoesNotExist:
				# TODO registrar
				_json['status'] = {
					'code' : 201,
					'msg' : "Registro Creado"
				}
				data = simplejson.dumps(_json)
				return HttpResponse(data)
		else:
			User.objects.get( username=username )
			_json['status'] = {
				'code' : 401,
				'msg' : "Error"
			}
			_json['data'] = {
				'errors':errors
			}
			data = simplejson.dumps(_json)
			return HttpResponse(data)
	else:
		_json['status'] = {
			'code' : 403,
			'msg' : "Forbidden"
		}
		data = simplejson.dumps(_json)
		return HttpResponse(data)

def logout(request):
	_json = {}
	auth_logout(request)
	_json['status'] = {
		'code' : 201,
		'msg' : "Ha salido de la aplicación exitosamente"
	}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

