#coding=utf-8
import string, random, time
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os


def upload(request):
	if not request.user.is_staff:
		raise Http404
	Rmsg=''
	if request.method == 'POST':
		try:
			destination = open('/www/upload/'+request.FILES['upload_file'].name,'wb+')
			for chunk in request.FILES['upload_file'].chunks(): 
				destination.write(chunk)
			destination.close()
			Rmsg='<a href="/download/'+request.FILES['upload_file'].name+'" target="_blank">http://121.41.24.81/download/'+request.FILES['upload_file'].name+'</a>'
		except:
			Rmsg='上传发生错误！'
	return render_to_response('upload.html',{'profile':request.user.profile,'msg':Rmsg,},context_instance=RequestContext(request))


def upload_cheetah(request):
	file_path='%s_%s' %(time.time(),string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 6)).replace(' ',''))
	try:
		os.mkdir('/www/upload/cheetah/'+file_path)
		destination = open('/www/upload/cheetah/'+file_path+'/'+request.FILES['file'].name,'wb+')
		for chunk in request.FILES['file'].chunks(): 
			destination.write(chunk)
		destination.close()
		return '/download/cheetah/'+file_path+'/'+request.FILES['file'].name
	except:
		return 'error'