#coding=utf-8
import string, random, time
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .settings import UPLUAD_DIR, UPLUAD_URL
import os


def basicupload(request,path,filename,key):
	try:
		try:
			destination = open(path+'/'+filename,'wb+')
		except:
			os.mkdir(path)
			destination = open(path+'/'+filename,'wb+')
		for chunk in request.FILES[key].chunks():
			destination.write(chunk)
		destination.close()
		return True
	except:
		return False

def upload_cheetah(request):
	file_path='%s_%s' %(time.time(),string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 6)).replace(' ',''))
	result=basicupload(request,UPLUAD_DIR+'/cheetah/'+file_path+'/',request.FILES['file'].name,'file')
	if result:
		return UPLUAD_URL+'/cheetah/'+file_path+'/'+request.FILES['file'].name
	else:
		return 'error'

def upload_page(request):
	if not request.user.is_staff:
		raise Http404
	Rmsg=''
	if request.method == 'POST':
		result=basicupload(request,UPLUAD_DIR+'/',request.FILES['upload_file'].name,'upload_file')
		if result:
			Rmsg='<a href="'+UPLUAD_URL+request.FILES['upload_file'].name+'" target="_blank">'+UPLUAD_URL+'/'+request.FILES['upload_file'].name+'</a>'
		else:
			Rmsg='上传发生错误！'
	return render_to_response('upload.html',{'profile':request.user.profile,'msg':Rmsg,},context_instance=RequestContext(request))

def upload_mpc(request):
	file_path='%s_' %(string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 6)).replace(' ',''))
	result=basicupload(request,UPLUAD_DIR+'/mpc/',file_path+request.FILES['upload_file'].name,'upload_file')
	if result:
		return UPLUAD_URL+'/mpc/'+file_path+request.FILES['upload_file'].name
	else:
		return 'error'
