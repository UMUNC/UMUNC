#coding=utf-8
import simplejson
from umunc import part_upload
from umunc_mpc.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def view_list(request,id=0):
    if id:
        response_list=Tag.objects.get(id=id).post_set.filter(status=True)
    else:
        response_list=Post.objects.filter(status=True)
    response_tag=Tag.objects.all()
    return render_to_response('umunc_mpc/list.html',{
        'posts':response_list,
        'tags':response_tag,
        'id':int(id),
        },context_instance=RequestContext(request))

def view_post(request, id):
    response_post=Post.objects.get(id=id)
    response_tag=Tag.objects.all()
    return render_to_response('umunc_mpc/post.html',{
        'post':response_post,
        'tags':response_tag
        },context_instance=RequestContext(request))

@login_required
def dashboard(request):
    if not request.user.is_staff:
        raise Http404
    response_msg=''
    response_tab=0
    if request.method=='GET' and request.GET.has_key('command'):
        if request.GET['command']=='GetPost':
            tpost=Post.objects.get(id=request.GET['id'])
            return HttpResponse(simplejson.dumps({
                'title':tpost.title,
                'content':tpost.content,
                'tags':[tag.id for tag in tpost.tag.all()],},ensure_ascii=False))
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

        if request.POST['command']=='TagAdd':
            if request.user.is_superuser:
                response_tab=1
                ttag=Tag(name=request.POST['name'])
                ttag.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='TagRename':
            if request.user.is_superuser:
                response_tab=1
                ttag=Tag.objects.get(id=request.POST['id'])
                ttag.name=request.POST['name']
                ttag.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='TagDelete':
            if request.user.is_superuser:
                response_tab=1
                ttag=Tag.objects.get(id=request.POST['id'])
                ttag.delete()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostCheck_R':
            if request.user.is_superuser:
                response_tab=2
                tpost=Post.objects.get(id=request.POST['id'])
                tpost.status=False
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostCheck_A':
            if request.user.is_superuser:
                response_tab=2
                tpost=Post.objects.get(id=request.POST['id'])
                tpost.status=True
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostDelete':
            tpost=Post.objects.get(id=request.POST['id'])
            if request.user.is_superuser or request.user==tpost.author:
                response_tab=2
                tpost.delete()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostNew':
            response_tab=2
            tpost=Post(
                title=request.POST['title'],
                content=request.POST['content'],
                author=request.user,
                status=False,)
            tpost.save()
            ttags=Tag.objects.all()
            for tag in ttags:
                if request.POST.has_key(str(tag.id)):
                    tpost.tag.add(tag)
            tpost.save()
        if request.POST['command']=='PostEdit':
            tpost=Post.objects.get(id=request.POST['id'])
            if request.user.is_superuser or request.user==tpost.author:
                response_tab=2
                tpost.title=request.POST['title']
                tpost.content=request.POST['content']
                tpost.author=request.user
                tpost.status=False
                tpost.tag.clear()
                ttags=Tag.objects.all()
                for tag in ttags:
                    if request.POST.has_key(str(tag.id)):
                        tpost.tag.add(tag)
                tpost.save()
            else:
                response_msg='无权操作'
    response_post=Post.objects.all()
    response_tag=Tag.objects.all()
    response_user=User.objects.all()
    return render_to_response('umunc_mpc/dashboard_post.html',{
        'msg':response_msg,
        'posts':response_post,
        'tags':response_tag,
        'tab':response_tab,
        'users':response_user
        },context_instance=RequestContext(request))


def dashboard_edit(request, id):
    response_post=Post.objects.get(id=id)
    response_tag=Tag.objects.all()
    return render_to_response('umunc_mpc/edit.html',{
        'post':response_post,
        'tags':response_tag
        },context_instance=RequestContext(request))
