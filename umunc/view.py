#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def default(request):
	return render_to_response('umunc/default.html',{},context_instance=RequestContext(request))
	
