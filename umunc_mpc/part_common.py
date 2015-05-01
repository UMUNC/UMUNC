#coding=utf-8
from django.contrib.auth.models import User

def user(request):
	return {'user':request.user,}