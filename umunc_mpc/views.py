#coding=utf-8
import simplejson
from umunc import part_upload
from umunc_mpc.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@vary_on_headers('Cookie')
@cache_page(5)
def view_list(request,pressname=''):

    response_press=cache.get('umunc_mpc_press_all')
    if response_press==None:
        response_press=Press.objects.all()
        cache.set('umunc_mpc_press_all',response_press)

    if pressname:
        tpress=response_press.get(name=pressname)

        response_list=cache.get('umunc_mpc_press_list_'+pressname)
        if response_list==None:
            response_list=tpress.post_set.filter(status=4)
            cache.set('umunc_mpc_press_list_'+pressname,response_list)

        response_list_gloable=cache.get('umunc_mpc_press_list_')
        if response_list_gloable==None:
            response_list_gloable=Post.objects.filter(status=4)
            cache.set('umunc_mpc_press_list_',response_list_gloable)

        response_template=cache.get('umunc_mpc_press_template_'+pressname)
        if response_template==None:
            response_template=response_press.get(name=pressname).template
            cache.set('umunc_mpc_press_template_'+pressname,response_template)
    else:
        response_list_gloable=cache.get('umunc_mpc_press_list_')
        if response_list_gloable==None:
            response_list_gloable=Post.objects.filter(status=4)
            cache.set('umunc_mpc_press_list_',response_list_gloable)

        response_list=response_list_gloable

        response_template='UMUNC'
    return render_to_response('umunc_mpc/list.html',{
        'posts':response_list,
        'posts_gloable':response_list_gloable[:5],
        'pressess':response_press,
        'pressname':pressname,
        'template':response_template,
        },context_instance=RequestContext(request))

@vary_on_headers('Cookie')
@cache_page(5)
def view_post(request,pressname,id):
    response_post=cache.get('umunc_mpc_post_'+id)
    if response_post==None:
        response_post=Post.objects.get(id=id)
        cache.set('umunc_mpc_post_'+id,response_post)

    response_press=cache.get('umunc_mpc_press_all')
    if response_press==None:
        response_press=Press.objects.all()
        cache.set('umunc_mpc_press_all',response_press)

    if pressname:
        tpress=response_press.get(name=pressname)
        if tpress not in response_post.press.all():
            raise Http404

        response_template=cache.get('umunc_mpc_press_template_'+pressname)
        if response_template==None:
            response_template=response_press.get(name=pressname).template
            cache.set('umunc_mpc_press_template_'+pressname,response_template)
    else:
        response_template='UMUNC'

    return render_to_response('umunc_mpc/post.html',{
        'post':response_post,
        'pressess':response_press,
        'pressname':pressname,
        'template':response_template,
        },context_instance=RequestContext(request))

def view_post_gloable(request,id):
    return view_post(request,'',id)

@login_required
def dashboard(request):
    # if not request.user.is_staff:
    #     raise Http404
    response_msg=''
    response_tab=0
    if request.method=='GET' and request.GET.has_key('command'):
        if request.GET['command']=='GetPressPostList':
            tpress=Press.objects.get(name=request.GET['pressname'])
            return render_to_response('umunc_mpc/dashboard_post_list.html',{
                'press':tpress
                },context_instance=RequestContext(request))
        if request.GET['command']=='GetPost':
            tpost=cache.get('umunc_mpc_post_'+request.GET['id'])
            if tpost==None:
                tpost=Post.objects.get(id=request.GET['id'])
                cache.set('umunc_mpc_post_'+request.GET['id'],tpost)

            return HttpResponse(simplejson.dumps({
                'title':tpost.title,
                'content':tpost.content,
                'pressess':[press.name for press in tpost.press.all()],},ensure_ascii=False))
    if request.method=='POST':
        if request.POST['command']=='ImageUpdate':
            content = request.FILES.get('upload_file', None)
            if content:
                if content.size>(2*1024*1024):
                    return HttpResponse(simplejson.dumps({
                        "success": False,
                        "msg": "文件超限,只接受2M以内文件。",
                        "file_path": "",
                        },ensure_ascii=False))
                result=part_upload.upload_mpc(request)
                if result=='error':
                    return HttpResponse(simplejson.dumps({
                        "success": False,
                        "msg": "服务器错误，请重试。",
                        "file_path": "",
                        },ensure_ascii=False))
                return HttpResponse(simplejson.dumps({
                    "success": True,
                    "file_path": result,
                    },ensure_ascii=False))
            else:
                return HttpResponse(simplejson.dumps({
                    "success": False,
                    "msg": "服务器错误，请重试。",
                    "file_path": "",
                    },ensure_ascii=False))

        if request.POST['command']=='PostCheck':
            tpost=cache.get('umunc_mpc_post_'+request.POST['id'])
            if tpost==None:
                tpost=Post.objects.get(id=request.POST['id'])
                cache.set('umunc_mpc_post_'+request.POST['id'],tpost)

            cache.delete('umunc_mpc_post_'+request.POST['id'])
            cache.delete('umunc_mpc_press_list_')
            for i in tpost.press.all():
                cache.delete('umunc_mpc_press_list_'+i.name)

            if request.user.is_staff or ((request.user==tpost.author)and(request.POST['status']=='2')):
                response_tab=request.POST['press']
                tpost.status=request.POST['status']
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostDelete':
            tpost=cache.get('umunc_mpc_post_'+request.POST['id'])
            if tpost==None:
                tpost=Post.objects.get(id=request.POST['id'])
                cache.set('umunc_mpc_post_'+request.POST['id'],tpost)

            cache.delete('umunc_mpc_post_'+request.POST['id'])
            cache.delete('umunc_mpc_press_list_')
            for i in tpost.press.all():
                cache.delete('umunc_mpc_press_list_'+i.name)

            if request.user.is_staff or ((request.user==tpost.author)and(tpost.status==1)):
                response_tab=request.POST['press']
                tpost.delete()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostNew':
            response_tab=request.POST['press']
            tpress=Press.objects.get(name=request.POST['press'])

            cache.delete('umunc_mpc_press_list_')

            if request.user.is_staff or (request.user in tpress.user.all()):
                tpost=Post(
                    title=request.POST['title'],
                    content=request.POST['content'],
                    author=request.user,
                    status=1,
                    level=0,)
                tpost.save()
                if request.user.is_staff:
                    tpresses=Press.objects.all()
                    for press in tpresses:
                        if request.POST.has_key(press.name):
                            tpost.press.add(press)
                            cache.delete('umunc_mpc_press_list_'+press.name)
                else:
                    tpost.press.add(tpress)
                    cache.delete('umunc_mpc_press_list_'+tpress.name)
                tpost.save()
        if request.POST['command']=='PostEdit':
            tpost=cache.get('umunc_mpc_post_'+request.POST['id'])
            if tpost==None:
                tpost=Post.objects.get(id=request.POST['id'])
                cache.set('umunc_mpc_post_'+request.POST['id'],tpost)

            cache.delete('umunc_mpc_post_'+request.POST['id'])
            cache.delete('umunc_mpc_press_list_')
            for i in tpost.press.all():
                cache.delete('umunc_mpc_press_list_'+i.name)

            if request.user.is_staff or ((request.user==tpost.author)and(tpost.status==1)):
                response_tab=request.POST['press']
                tpost.title=request.POST['title']
                tpost.content=request.POST['content']
                if request.user.is_staff:
                    tpost.press.clear()
                    tpresses=Press.objects.all()
                    for press in tpresses:
                        cache.delete('umunc_mpc_press_list_'+press.name)
                        if request.POST.has_key(press.name):
                            tpost.press.add(press)
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostLevel':
            tpost=cache.get('umunc_mpc_post_'+request.POST['id'])
            if tpost==None:
                tpost=Post.objects.get(id=request.POST['id'])
                cache.set('umunc_mpc_post_'+request.POST['id'],tpost)

            cache.delete('umunc_mpc_post_'+request.POST['id'])
            cache.delete('umunc_mpc_press_list_')
            for i in tpost.press.all():
                cache.delete('umunc_mpc_press_list_'+i.name)

            if request.user.is_staff:
                response_tab=request.POST['press']
                tpost.level=request.POST['level']
                tpost.save()
            else:
                response_msg='无权操作'

    if request.user.is_staff:
        response_press=Press.objects.all()
    else:
        response_press=request.user.press_set.all()
    # response_post=Post.objects.all()
    # response_tag=Tag.objects.all()
    # response_user=User.objects.all()
    return render_to_response('umunc_mpc/dashboard_post.html',{
        'presses':response_press,
        # 'msg':response_msg,
        # 'posts':response_post,
        # 'tags':response_tag,
        'tab':response_tab,
        # 'users':response_user
        },context_instance=RequestContext(request))


def dashboard_edit(request, id):
    response_post=Post.objects.get(id=id)
    response_tag=Tag.objects.all()
    return render_to_response('umunc_mpc/edit.html',{
        'post':response_post,
        'tags':response_tag
        },context_instance=RequestContext(request))
