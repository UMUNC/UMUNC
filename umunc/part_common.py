#coding=utf-8
import string, random, time
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os

def check_arguments(list,accept):
	for i in accept:
		if not list.has_key(i):
			return False
	return True

def public_gloable(request,dict):
	dict['user']=request.user
	return dict