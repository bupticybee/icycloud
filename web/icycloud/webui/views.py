from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import random
import datetime
import json
import traceback
from webui.tasks import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as login_auth,logout as logout_auth

def isvalid(domain):
    for i in domain:
        if i not in 'abcdefghijklmnopqrstuvwxyz-0123456789':
            return False
    return True

def retjson(retval):
    return HttpResponse(json.dumps(retval),content_type='application/json')

# Create your views here.
def index(request):
    #add.delay(4,4)
    #return HttpResponse(html)
    data = {
        'user':request.user.is_authenticated(),
    }
    return render(request,'webui/index.html',data)

def about(request):
    #add.delay(4,4)
    #return HttpResponse(html)
    data = {
        'user':request.user.is_authenticated(),
    }
    return render(request,'webui/about.html',data)

def invitecode(request):
    return render(request,'webui/invitecode.html',{'user':request.user.is_authenticated()})

def register(request):
    invitecode = request.POST.get('invitecode')
    if invitecode == None:
        return render(request,'webui/invitecode.html')
    if not InviteCode.objects.filter(code=invitecode,used=False):
        return render(request,'webui/invitecode.html',{'wrong':1})
    invitecode = invitecode.strip()
    return render(request,'webui/register.html',{'invitecode':invitecode.strip(),'user':request.user.is_authenticated()})

def register_api(request):
    username = 		request.POST.get('username')
    password = 		request.POST.get('password')
    repassword = 	request.POST.get('repassword')
    email = 		request.POST.get('email')
    invitecode = 	request.POST.get('invitecode')
    if not (username and password and repassword and invitecode):
        retval = {
            'result':'failed',
            'errmsg':'empty param'
        }
        return retjson(retval)
    if not InviteCode.objects.filter(code=invitecode,used=False):
        retval = {
            'result':'failed',
            'errmsg':'invalid invitecode'
        }
        return retjson(retval)

    if not isvalid(username):
        retval = {
            'result':'failed',
            'errmsg':'invalid username'
        }
        return retjson(retval)

    if not (len(password) > 6 and password == repassword):
        retval = {
            'result':'failed',
            'errmsg':'password invalid'
        }
        return retjson(retval)

    if User.objects.filter(username=username):
        retval = {
            'result':'failed',
            'errmsg':'user already exist',
        }
        return retjson(retval)

    try:
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        clouduser = CloudUser(user=user)
        clouduser.save()
    except: 
        e = traceback.format_exc()
        retval = {
            'result':'failed',
            'errmsg':'create user fail',
            'debuginfo':e,
        }
        return retjson(retval)

    invitecodeobj = InviteCode.objects.filter(code=invitecode)
    invitecodeobj.delete()
    retval = {
        'result':'success',
    }
    return retjson(retval)

def generate_invite_code(number):
    retval = []
    for i in range(number):
        invstr = ""
        for j in range(20):
            invstr += random.choice('abcdefghijklmnopqrstuvwxyz-0123456789')
        retval.append(invstr)
    return retval
 
@staff_member_required
def publish_invitecode(request):
    number = request.POST.get('number')
    if not number:
        data = {
            'user':request.user.is_authenticated(),
        }
        return render(request,'webui/publish_invitecode.html',data)
    else:
        number = int(number)
        assert(number > 0 and number < 100)
        invitecodes = generate_invite_code(number)
        for code in invitecodes:
            invobj = InviteCode.objects.filter(code=code)
            if invobj:
                invobj.used = True
                invobj.save()
            else:
                invobj = InviteCode(code=code)
                invobj.save()
        data = {
            'invitecodes':invitecodes,
            'user':request.user.is_authenticated(),
        }
        return render(request,'webui/publish_invitecode.html',data)
    url(r'register$', views.register, name='register'),

@login_required(login_url="/login")
def console(request):
    user = request.user
    machines = Machine.objects.filter(user=user)
    disabled = True
    try:
        maxmachine = user.clouduser.maxmachine  
        currentmachines = len(Machine.objects.filter(user=user))
        if maxmachine > currentmachines:
            disabled = False
    except:
        pass
    for machine in machines:
        if machine.status == 'C':
            machine.machinestatus = 'Creating...'
        elif machine.status == 'R':
            machine.machinestatus = 'Running'
        elif machine.status == 'D':
            machine.machinestatus = 'Down'
        elif machine.status == 'F':
            machine.machinestatus = 'Failed'
        else:
            machine.machinestatus = 'failed to get status'
    for machine in machines:
        machineip = machine.machineip
        if Router.objects.filter(machineip=machineip):
            machine.bindurl = Router.objects.filter(machineip=machineip)[0].url
        else:
            machine.bindurl = ''
    data = {
        'machines':machines,
        'disabled':disabled,
        'user':request.user.is_authenticated(),
    }
    return render(request,'webui/console.html',data)

def login(request):
    nextpage = request.GET.get('next')
    if nextpage == None:
        nextpage = request.POST.get('next')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login_auth(request, user)
        if nextpage and nextpage != 'None':
            return HttpResponseRedirect(nextpage)
        return HttpResponseRedirect('/console')
    return render(request,'webui/login.html',{'next':nextpage,'user':request.user.is_authenticated()})

def logout(request):
    logout_auth(request)
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
def create_machine(request):
    user = request.user
    os = request.POST.get('os')
    password = request.POST.get('password')
    repassword = request.POST.get('repassword')
    if len(password) < 4 or password != repassword:
        retval = {
            'result':'failed',
            'errmsg':'password invalid'
        }
        return HttpResponseRedirect('/console')
    createMachine.delay(user.username,os,password)
    #return HttpResponse(html)
    return HttpResponseRedirect('/console')

