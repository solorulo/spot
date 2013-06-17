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
