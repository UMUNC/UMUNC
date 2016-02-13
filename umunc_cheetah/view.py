#coding=utf-8
import string, random, time, simplejson
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from umunc_cheetah.models import *
from umunc_iris.models import *
from umunc import part_upload
from umunc.settings import TIME_DIR, REFRESH_DIR

@login_required
def default(request):
	if request.user.is_staff==False:
		response_rooms=request.user.room_set.all()
		response_rooms_a=room.objects.all()
	else:
		response_rooms=room.objects.all()
		response_rooms_a=response_rooms
	response_meetings=meeting.objects.all()
	response_countries=country.objects.all()
	return render_to_response('umunc_cheetah/default.html',{
		'rooms':response_rooms,
		'meetings':response_meetings,
		'countries':response_countries,
		'rooms_a':response_rooms_a,
		},context_instance=RequestContext(request))

def history_communication(request,id):
	response_room=room.objects.get(id=id)
	if not (request.user in response_room.User.all()):
		return HttpResponse('通讯房间无权进入。')
	response_messages=message.objects.filter(ToU=response_room)
	return render_to_response('umunc_cheetah/history_communication.html',{
		'room':response_room,
		'messages':response_messages,
		},context_instance=RequestContext(request))

def history_meeting(request):
	if request.user.is_staff:
		if request.user.profile.Country:
			number=str(request.user.profile.Country.id)+'_A'
		else:
			number=str(0)+'_A'
	else:
		if request.user.profile.Country:
			number=str(request.user.profile.Country.id)
		else:
			number=str(0)
	if request.user.is_staff:
		response_meetings=meeting.objects.all()
	else:
		response_meetings=meeting.objects.filter(Q(FromC=request.user.profile.Country)|Q(ToC=request.user.profile.Country))
	return render_to_response('umunc_cheetah/history_meeting.html',{
			'meetings': response_meetings,
		},context_instance=RequestContext(request))

def refresh_communication_list():
	response_rooms=room.objects.all()
	ttemplate = get_template('umunc_cheetah/datacontrol_communication_list.html')
	cache.set('umunc_cheetah_communication_list',ttemplate.render(Context({'rooms':response_rooms})))

def refresh_communiaction(troom,request,number):
	response_messages=message.objects.filter(ToU=troom)[:50]
	ttemplate = get_template('umunc_cheetah/datacontrol_communication.html')
	cache.set('umunc_cheetah_communication_'+number, simplejson.dumps({
		'result':'success',
		'messages':ttemplate.render(Context({'messages': response_messages,'user':request.user,'room':troom})),
		'room':{'Name':troom.Name,'Block':troom.Block,},
		'staff':request.user.is_staff,
		'count':response_messages.count(),
		},ensure_ascii=False),None)
	refresh_communication_list()

def refresh_meeting(user,number):
	if user.is_staff:
		response_meetings=meeting.objects.all()
	else:
		response_meetings=meeting.objects.filter(Q(FromC=user.profile.Country)|Q(ToC=user.profile.Country))
	ttemplate = get_template('umunc_cheetah/datacontrol_meeting.html')
	cache.set('umunc_cheetah_meeting_'+number, simplejson.dumps({
				'result':'success',
				'meeting':ttemplate.render(Context({'meetings': response_meetings,'user':user})),
				'count':response_meetings.count(),
				},ensure_ascii=False),None)

def refresh_meeting_list(user,number):
	cache.set('umunc_cheetah_meeting_'+number+'_list',str(time.time())+',',None)

def refresh_meeting_couple(fcountry,tcountry,request):
	cache.delete('umunc_cheetah_meeting_'+str(fcountry.id))
	cache.delete('umunc_cheetah_meeting_'+str(tcountry.id))
	cache.delete('umunc_cheetah_meeting_'+str(0))
	cache.delete('umunc_cheetah_meeting_'+str(0)+'_A')
	cache.delete('umunc_cheetah_meeting_'+str(fcountry.id)+'_list')
	cache.delete('umunc_cheetah_meeting_'+str(tcountry.id)+'_list')
	cache.delete('umunc_cheetah_meeting_'+str(0)+'_list')
	cache.delete('umunc_cheetah_meeting_'+str(0)+'_A'+'_list')
	tcountries=country.objects.all()
	for tcountry in tcountries:
		cache.delete('umunc_cheetah_meeting_'+str(tcountry.id)+'_A')
		cache.delete('umunc_cheetah_meeting_'+str(tcountry.id)+'_A'+'_list')

def refresh_virtualtime():
	destination = open(TIME_DIR,'r')
	t=destination.readline()
	destination.close()
	cache.set('umunc_cheetah_virtualtime', t,None)

def check_refresh():
	destination = open(REFRESH_DIR,'r')
	t=destination.readline()
	destination.close()
	return t[:7]

@login_required
def datacontrol_heartbeat(request):
	if request.GET.has_key('command'):
		if request.GET['command']=='GetHeartBeat':
			if check_refresh()=='REFRESH':
				return HttpResponse(simplejson.dumps({
				'messages':'REFRESH',},ensure_ascii=False),None)
			if cache.get('umunc_cheetah_communication_list')==None:
				refresh_communication_list()
			if request.user.is_staff:
				if request.user.profile.Country:
					number=str(request.user.profile.Country.id)+'_A'
				else:
					number=str(0)+'_A'
			else:
				if request.user.profile.Country:
					number=str(request.user.profile.Country.id)
				else:
					number=str(0)
			if cache.get('umunc_cheetah_meeting_'+number+'_list')==None:
				refresh_meeting_list(request.user,number)
			if cache.get('umunc_cheetah_virtualtime')==None:
				refresh_virtualtime()
			return HttpResponse(
				'{"communication":'+cache.get('umunc_cheetah_communication_list')+
				'"meeting":'+cache.get('umunc_cheetah_meeting_'+number+'_list')+
				'"virtualtime":'+cache.get('umunc_cheetah_virtualtime')+
				'}')
		if request.GET['command']=='GetCommunication' and request.GET.has_key('number'):
			troom=room.objects.get(id=request.GET['number'])
			if not (request.user in troom.User.all()):
				return HttpResponse(simplejson.dumps({'result':'通讯房间无权进入。',},ensure_ascii=False))
			if cache.get('umunc_cheetah_communication_'+request.GET['number'])==None:
				refresh_communiaction(troom,request,request.GET['number'])
			return HttpResponse(cache.get('umunc_cheetah_communication_'+request.GET['number']))
		if request.GET['command']=='GetMeeting':
			if request.user.is_staff:
				if request.user.profile.Country:
					number=str(request.user.profile.Country.id)+'_A'
				else:
					number=str(0)+'_A'
			else:
				if request.user.profile.Country:
					number=str(request.user.profile.Country.id)
				else:
					number=str(0)
			if cache.get('umunc_cheetah_meeting_'+number)==None:
				refresh_meeting(request.user,number)
			return HttpResponse(cache.get('umunc_cheetah_meeting_'+number))


@login_required
def datacontrol_communication(request):
	response_rooms=room.objects.all()
	if request.POST.has_key('command'):
		if request.POST['command']=='PostSend' and request.POST.has_key('system') and request.POST.has_key('number') and request.POST.has_key('content'):
			troom=room.objects.get(id=request.POST['number'])
			if not (request.user in troom.User.all()):
				return HttpResponse(simplejson.dumps({'result':'通讯房间无权进入。',},ensure_ascii=False))
			if troom.Block and request.user.is_staff==False:
				return HttpResponse(simplejson.dumps({'result':'房间禁言。',},ensure_ascii=False))
			if request.POST['system']=='true' and request.user.is_staff==False:
				return HttpResponse(simplejson.dumps({'result':'无权发表系统消息。',},ensure_ascii=False))
			tmessage=message(
				FromU=request.user,
				ToU=troom,
				Content=request.POST['content'],
				System=request.POST['system']=='true',)
			tmessage.save()
			refresh_communiaction(troom,request,request.POST['number'])
			return HttpResponse(simplejson.dumps({
				'result':'success',
				},ensure_ascii=False))
		if request.POST['command']=='PostSendAll' and request.POST.has_key('content'):
			if  request.user.is_staff==False:
				return HttpResponse(simplejson.dumps({'result':'无权发表消息。',},ensure_ascii=False))
			troom_a=room.objects.all()
			for troom in troom_a:
				tmessage=message(
					FromU=request.user,
					ToU=troom,
					Content=request.POST['content'],
					System=True,)
				tmessage.save()
				refresh_communiaction(troom,request,str(troom.id))
			return HttpResponse(simplejson.dumps({
				'result':'success',
				},ensure_ascii=False))
		if request.POST['command']=='PostBlock' and request.POST.has_key('number'):
			troom=room.objects.get(id=request.POST['number'])
			if not (request.user in troom.User.all()):
				return HttpResponse(simplejson.dumps({'result':'通讯房间无权进入。',},ensure_ascii=False))
			if request.user.is_staff==False:
				return HttpResponse(simplejson.dumps({'result':'无权修改。',},ensure_ascii=False))
			if troom.Block:
				tcontent='管理员已关闭禁言'
			else:
				tcontent='管理员已开启禁言'
			troom.Block=not troom.Block
			troom.save()
			tmessage=message(
				FromU=request.user,
				ToU=troom,
				Content=tcontent,
				System=True,)
			tmessage.save()
			refresh_communiaction(troom,request,request.POST['number'])
			return HttpResponse(simplejson.dumps({
				'result':'success',
				},ensure_ascii=False))

@login_required
def datacontrol_meeting(request):
	response_rooms=room.objects.all()
	if request.POST.has_key('command'):
		if request.POST['command']=='PostSend' and request.POST.has_key('host') and request.POST.has_key('to') and request.POST.has_key('location') and request.POST.has_key('time') and request.POST.has_key('description'):
			fcountry=country.objects.get(id=request.POST['host'])
			tcountry=country.objects.get(id=request.POST['to'])
			if request.user.profile.Country!=fcountry and request.user.is_staff==False:
				return HttpResponse(simplejson.dumps({'result':'无权发表系统消息。',},ensure_ascii=False))
			tmeeting=meeting(
				FromC=fcountry,
				ToC=tcountry,
				Time=request.POST['time'],
				Location=request.POST['location'],
				Description=request.POST['description'],
				Check_F=True,
				Check_T=None,
				Check_A=True,)
			tmeeting.save()
			refresh_meeting_couple(fcountry,tcountry,request)
			return HttpResponse(simplejson.dumps({
				'result':'success',
				},ensure_ascii=False))
		if request.POST['command']=='PostChange' and request.POST.has_key('user_number') and request.POST.has_key('number') and request.POST.has_key('accept'):
			tmeeting=meeting.objects.get(id=request.POST['number'])
			if request.POST['user_number']=='0':
				if request.user.is_staff==False:
					return HttpResponse(simplejson.dumps({'result':'无权操作。',},ensure_ascii=False))
				if tmeeting.Check_A!=False:
					tmeeting.Check_A=request.POST['accept']=='1'
					tmeeting.save()
					refresh_meeting_couple(tmeeting.FromC,tmeeting.ToC,request)
				return HttpResponse(simplejson.dumps({'result':'success',},ensure_ascii=False))
			elif request.POST['user_number']=='1':
				if request.user.profile.Country!=tmeeting.FromC:
					return HttpResponse(simplejson.dumps({'result':'无权操作。',},ensure_ascii=False))
				if tmeeting.Check_F!=False:
					tmeeting.Check_F=request.POST['accept']=='1'
					tmeeting.save()
					refresh_meeting_couple(tmeeting.FromC,tmeeting.ToC,request)
				return HttpResponse(simplejson.dumps({'result':'success',},ensure_ascii=False))
			elif request.POST['user_number']=='2':
				if request.user.profile.Country!=tmeeting.ToC:
					return HttpResponse(simplejson.dumps({'result':'无权操作。',},ensure_ascii=False))
				if tmeeting.Check_T!=False:
					tmeeting.Check_T=request.POST['accept']=='1'
					tmeeting.save()
					refresh_meeting_couple(tmeeting.FromC,tmeeting.ToC,request)
				return HttpResponse(simplejson.dumps({'result':'success',},ensure_ascii=False))

@login_required
def datacontrol_file(request):
	if request.method == 'POST' and request.POST.has_key('to'):
		troom=room.objects.get(id=request.POST['to'])
		content = request.FILES.get('file', None)
		if content:
			if content.size>(2*1024*1024):
				return HttpResponse(simplejson.dumps({'result':'文件超限,只接受2M以内文件。',},ensure_ascii=False))
			result=part_upload.upload_cheetah(request)
			if result=='error':
				return HttpResponse(simplejson.dumps({'result':'服务器错误，请重试。',},ensure_ascii=False))
			ttemplate = get_template('umunc_cheetah/datacontrol_file.html')
			tmessage=message(
				FromU=request.user,
				ToU=troom,
				Content=ttemplate.render(Context({'filename':request.FILES['file'].name,'url':result,'user':request.user})),
				System=True,)
			tmessage.save()
			refresh_communiaction(troom,request,request.POST['to'])
			return HttpResponse(simplejson.dumps({'result':'success','url':result,},ensure_ascii=False))
		else:
			return HttpResponse(simplejson.dumps({'result':'服务器错误，请重试。',},ensure_ascii=False))

@login_required
def datacontrol_setting(request):
	if request.POST.has_key('command'):
		if request.POST['command']=='ClearRefresh':
			if request.user.is_staff:
				cache.clear()
				return HttpResponse('success')
			else:
				return HttpResponse('无权操作。')
		if request.POST['command']=='FrontendRefresh':
			if request.user.is_staff:
				destination = open(REFRESH_DIR,'wd+')
				destination.write('REFRESH')
				destination.close()
				time.sleep(4)
				destination = open(REFRESH_DIR,'wd+')
				destination.write('NONE')
				destination.close()
				return HttpResponse('success')
			else:
				return HttpResponse('无权操作。')
		if request.POST['command']=='Time' and request.POST.has_key('BaseTime') and request.POST.has_key('VirtualBaseTime') and request.POST.has_key('TimeStep'):
			destination = open(TIME_DIR,'wd+')
			destination.writelines('{"vtime_base":'+request.POST['BaseTime']+',"vtime_check":'+request.POST['VirtualBaseTime']+',"vtime_step":'+request.POST['TimeStep']+'}')
			destination.close()
			return HttpResponse(simplejson.dumps({
				'result':'success',
				},ensure_ascii=False))
