#coding=utf-8
import simplejson
from umunc import part_upload
from umunc_mpc.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def view_list(request,pressname=''):
    response_editable=False
    if request.user.is_staff:
        response_editable=True
    elif pressname and (request.user in Press.objects.get(name=pressname).user.all()):
        response_editable=True

    if pressname:
        response_list=Press.objects.get(name=pressname).post_set.filter(status=4)
        response_template=Press.objects.get(name=pressname).template
        response_list_gloable=Post.objects.filter(status=4)
    else:
        response_list=Post.objects.filter(status=4)
        response_template='UMUNC'
        response_list_gloable=Post.objects.filter(status=4)
    response_press=Press.objects.all()
    return render_to_response('umunc_mpc/list.html',{
        'posts':response_list,
        'posts_gloable':response_list_gloable[:5],
        'pressess':response_press,
        'pressname':pressname,
        'editable':response_editable,
        'template':response_template,
        },context_instance=RequestContext(request))

def view_post(request,pressname,id):
    response_editable=False
    if request.user.is_staff:
        response_editable=True
    elif pressname and (request.user in Press.objects.get(name=pressname).user.all()):
        response_editable=True

    response_post=Post.objects.get(id=id)
    response_press=Press.objects.all()
    if pressname:
        response_template=Press.objects.get(name=pressname).template
        tpress=Press.objects.get(name=pressname)
        response_template=Press.objects.get(name=pressname).template
        if tpress not in response_post.press.all():
            raise Http404
    else:
        response_template=''
        response_template='UMUNC'

    return render_to_response('umunc_mpc/post.html',{
        'post':response_post,
        'pressess':response_press,
        'pressname':pressname,
        'editable':response_editable,
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
            tpost=Post.objects.get(id=request.GET['id'])
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
            tpost=Post.objects.get(id=request.POST['id'])
            if request.user.is_staff or ((request.user==tpost.author)and(request.POST['status']=='2')):
                response_tab=request.POST['press']
                tpost.status=request.POST['status']
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostDelete':
            tpost=Post.objects.get(id=request.POST['id'])
            if request.user.is_staff or ((request.user==tpost.author)and(tpost.status==1)):
                response_tab=request.POST['press']
                tpost.delete()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostNew':
            response_tab=request.POST['press']
            tpress=Press.objects.get(name=request.POST['press'])
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
                else:
                    tpost.press.add(tpress)
                tpost.save()
        if request.POST['command']=='PostEdit':
            tpost=Post.objects.get(id=request.POST['id'])
            if request.user.is_staff or ((request.user==tpost.author)and(tpost.status==1)):
                response_tab=request.POST['press']
                tpost.title=request.POST['title']
                tpost.content=request.POST['content']
                if request.user.is_staff:
                    tpost.press.clear()
                    tpresses=Press.objects.all()
                    for press in tpresses:
                        if request.POST.has_key(press.name):
                            tpost.press.add(press)
                tpost.save()
            else:
                response_msg='无权操作'
        if request.POST['command']=='PostLevel':
            tpost=Post.objects.get(id=request.POST['id'])
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
