# -*- coding: utf-8 -*-
# Create your views here.
import os
from spot_app.models import *
import datetime 
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
	# try:
	if not request.user.is_authenticated():
		_json['status'] = {
			'code' : 401,
			'msg' : "Sesion no iniciada"
		}
		data = simplejson.dumps(_json)
		return HttpResponse(data)

	if request.method != "POST" :
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

	current_datetime = datetime.datetime.now()
	delayVal = current_datetime + datetime.timedelta(minutes = int(delay))

	new_foto = Photo(
		picture=foto_id, 
		user=request.user, 
		delay=delayVal,
		description=desc,
		urbex=urbex,
		lat=lat,
		lng=lng,
		xAccel=0,
		yAccel=0,
		zAccel=0,
		other="")
	new_foto.save()
	_json['status'] = {
		'code' : 201,
		'msg' : "Bien"
	}

	# except:
	# 	_json['status'] = {
	# 		'code' : 500,
	# 		'msg' : "Internal Error"
	# 	}
	data = simplejson.dumps(_json)
	return HttpResponse(data)

def photo(request):
	_json = {}
	# try:
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

	foto_id = request.GET['id_image']

	foto = Photo.objects.get(pk=foto_id)
	foto_user = foto.user

	anonimo = foto.anonymous

	likes = Like.objects.filter(photo_id=foto.pk).order_by('-pk')[:4]
	# count_likes = likes.count()
	last_likes = []
	for lk in likes:
		last_likes.append({
			'name':lk.user.username
			})

	comments_db = Comment.objects.all().order_by('-pk')[:10]
	comments = []
	for comment in comments_db:
		info_user = Info_User.objects.get(user__pk=comment.user.pk)
		cmnt = {
			'username':comment.user.username,
			'text':comment.text
		}
		if info_user.picture:
			cmnt['user_pic_url'] = url(info_user.picture, height=300)
			cmnt['user_pic_public_id'] = info_user.picture.public_id
		comments.append(cmnt)


	_json['status'] = {
		'code' : 200,
		'msg' : "Bien"
	}
	_json['data'] = {
		'pic_url':url(foto.picture, height=600),
		'pic_public_id':foto.picture.public_id,
		'description':foto.description,
		'n_likes':Like.objects.filter(photo=foto).count(),
		'last_likes':last_likes,
		'comments':comments
	}

	if not anonimo :
		info_user = Info_User.objects.get(user__pk=foto_user.pk)
		_json['data']['user_id'] = foto_user.pk
		_json['data']['user_name'] = foto_user.username

		if info_user.foto_url:
			_json['data']['user_pic_url'] = url(info_user.picture, height=300)
			_json['data']['user_pic_public_id'] = info_user.picture.public_id

	# except:
	# 	_json['status'] = {
	# 		'code' : 500,
	# 		'msg' : "Internal Error"
	# 	}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
