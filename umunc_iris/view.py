#coding=utf-8
import string, random, time
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from umunc import part_mail, part_upload
from umunc_iris.models import *
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
import re

@login_required
def test(request):
	return HttpResponseRedirect('/cheetah')

def temp(request):
	return HttpResponse('IRIS已关闭')

@login_required
def default(request):
	return render_to_response('umunc_iris/default.html',{'profile':request.user.profile},context_instance=RequestContext(request))

def plogin(request):
	Rusername=''
	Rpassword=''
	Rerror=''
	Rnext=''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.POST.has_key('username') and request.POST.has_key('password'):
		Rusername = request.POST['username']
		Rpassword = request.POST['password']
		Rnext=request.POST['next']
		user = authenticate(username=Rusername, password=Rpassword)
		if user is not None:
			if user.profile.Status<>0:
				login(request, user)
				return HttpResponseRedirect(Rnext)
			else:
				Rerror='此账号未验证邮箱，请验证后再试。'
		else:
			Rerror='登录失败，请确认用户名密码正确。'
	else:
		Rnext=request.GET.get('next')
		if not Rnext:Rnext='/'
	return render_to_response('umunc_iris/login.html',{
		'username':Rusername,
		'error':Rerror,
		'next':Rnext,},context_instance=RequestContext(request))

def pregister(request):
	Rusername=''
	Rpassword=''
	Rerror=''
	Remail=''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.POST.has_key('username') and request.POST.has_key('password') and request.POST.has_key('email'):
		Rusername = request.POST['username']
		Rpassword = request.POST['password']
		Remail = request.POST['email']
		user = User.objects.filter(username = Rusername)
		if not user:
			tuser = User.objects.create_user(
				username=Rusername,
				email=Remail,
				password=Rpassword,)
			tuser.is_active = True
			tuser.save()
			tprofile = profile(
				User=tuser,
				Leader=False,
				Init=True,
				Name='',
				Sex=True,
				Age=0,
				IDNum='',
				School='',
				Grade=1,
				GName='',
				GPhone='',
				Phone='',
				Phone2='',
				QQ='',
				Wechat='',
				MunAge=0,
				MunRsm='',
				MunJoined=False,
				Commitee=1,
				Review='',
				Status=0,)
			tprofile.save()
			tcheckcode_code = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 32)).replace(' ','')
			tcheckcode = checkcode(
				User = tuser,
				CheckCode = tcheckcode_code,)
			tcheckcode.save()
			part_mail.sendmail_emailcheck(request.POST['email'],request.POST['username'],tcheckcode_code)
			Rerror='success'
		else:
				Rerror='此账号已存在。'
	return render_to_response('umunc_iris/register.html',{
		'username':Rusername,
		'error':Rerror,
		'email':Remail,},context_instance=RequestContext(request))

def pcheck(request):
	Rerror='1'
	if request.GET.has_key('checkcode'):
		try:
			tcheckcode = checkcode.objects.get(CheckCode=request.GET['checkcode'])
			tuser = tcheckcode.User
			tprofile = tcheckcode.User.profile
			tprofile.Status = 1
			tprofile.save()
			tcheckcode.delete()
			Rerror=''
		except:
			pass
		return render_to_response('umunc_iris/check.html',{
			'error':Rerror,
		},context_instance=RequestContext(request))

def plogout(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required
def pchange(request):
	Rerror=''
	if request.POST.has_key('password') and request.POST.has_key('password1'):
		Rpassword = request.POST['password']
		Rpassword1 = request.POST['password1']
		user = authenticate(username=request.user.username, password=Rpassword)
		if user is not None:
			request.user.set_password(Rpassword1)
			request.user.save()
			request.user.profile.Init=True;
			request.user.profile.save()
			Rerror='success'
		else:
			Rerror='密码错误，请确认原密码正确。'
	return render_to_response('umunc_iris/change.html',{'error':Rerror,},context_instance=RequestContext(request))

@login_required
def step1(request):
	if request.POST.has_key('name') and request.POST.has_key('sex') and request.POST.has_key('age') and request.POST.has_key('idnum') and request.POST.has_key('school') and request.POST.has_key('grade') and request.POST.has_key('phone') and request.POST.has_key('phone2') and request.POST.has_key('qq') and request.POST.has_key('wechat') and request.POST.has_key('gname') and request.POST.has_key('gphone') and request.POST.has_key('munage') and request.POST.has_key('munrsm') and request.POST.has_key('commitee') and request.POST.has_key('commitee2') and request.POST.has_key('adjust') and request.POST.has_key('submit'):
		request.user.profile.Name=request.POST['name']
		request.user.profile.Sex=(request.POST['sex']=='1')
		request.user.profile.Age=request.POST['age']
		request.user.profile.IDNum=request.POST['idnum']
		request.user.profile.School=request.POST['school']
		request.user.profile.Grade=request.POST['grade']
		request.user.profile.GName=request.POST['gname']
		request.user.profile.GPhone=request.POST['gphone']
		request.user.profile.Phone=request.POST['phone']
		request.user.profile.Phone2=request.POST['phone2']
		request.user.profile.QQ=request.POST['qq']
		request.user.profile.Wechat=request.POST['wechat']
		request.user.profile.MunAge=request.POST['munage']
		request.user.profile.MunRsm=request.POST['munrsm']
		request.user.profile.Commitee=request.POST['commitee']
		request.user.profile.Commitee2=request.POST['commitee2']
		request.user.profile.Adjust=(request.POST['adjust']=='1')
		if request.POST['submit']=='1':
			request.user.profile.Status=2
		request.user.profile.save()
		return HttpResponseRedirect('/iris/step1')
	return render_to_response('umunc_iris/step1.html',{'profile':request.user.profile},context_instance=RequestContext(request))

@login_required
def step2(request):
	Rerror=''
	Rgroups=group.objects.filter(Group=True)
	if request.POST.has_key('name') and request.POST.has_key('school') and request.POST.has_key('password') and request.POST.has_key('class') and request.POST.has_key('group'):
		if request.POST['class']=='1':
			try:
				tgroup=group.objects.get(Name= request.POST['name'])
			except:
				tgroup = group(
					Name=request.POST['name'],
					School=request.POST['school'],
					Password=request.POST['password'],
					Payment=False,
					Group=True,)
				tgroup.save()
				request.user.profile.Group=tgroup
				request.user.profile.Leader=True
				request.user.profile.Status=3
				request.user.profile.save()
				Rerror='success'
			else:
				Rerror='该团体名称已存在。'
		if request.POST['class']=='2':
			try:
				tgroup=group.objects.get(Name= request.POST['group'])
			except:
				Rerror='该团体不存在。'
			else:
				if tgroup.Password==request.POST['password']:
					tgroup=group.objects.get(Name= request.POST['group'])
					request.user.profile.Group=tgroup
					request.user.profile.Leader=False
					request.user.profile.Status=3
					request.user.profile.save()
					Rerror='success'
				else:
					Rerror='口令错误。'
		if request.POST['class']=='3':
			tcode = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 32)).replace(' ','') + request.user.username
			tgroup = group(
				Name=tcode,
				School='none',
				Password='none',
				Payment=False,
				Group=False,)
			tgroup.save()
			request.user.profile.Group=tgroup
			request.user.profile.Leader=True
			request.user.profile.Status=3
			request.user.profile.save()
			Rerror='success'
	return render_to_response('umunc_iris/step2.html',{'profile':request.user.profile,'error':Rerror,'groups':Rgroups,},context_instance=RequestContext(request))

@login_required
def step3(request):
	if request.POST.has_key('review') and request.POST.has_key('submit'):
		request.user.profile.Review=request.POST['review']
		if request.POST['submit']=='1':
			request.user.profile.Status=4
		request.user.profile.save()
		return HttpResponseRedirect('/iris/step3')
	return render_to_response('umunc_iris/step3.html',{'profile':request.user.profile,},context_instance=RequestContext(request))


@login_required
def step4(request):
	return render_to_response('umunc_iris/step4.html',{'profile':request.user.profile,},context_instance=RequestContext(request))

