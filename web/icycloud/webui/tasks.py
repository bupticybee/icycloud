from celery import task
from docker import Client
from .models import *
from django.contrib.auth.models import User
import time

@task
def add(x,y):
	cli = Client(base_url='unix://var/run/docker.sock')
	print cli.images()
	return x + y

@task
def createMachine(username,osname,password):
	user = User.objects.get(username=username)
	maxmachine = user.clouduser.maxmachine
	machines = len(Machine.objects.filter(user=user))
	if machines >= maxmachine:
		print 'already have enought machine'
		return
	namedic = {
		'ubuntu 14.04':'icycloud/ubuntu-baseimage:0.9.18',
		'ubuntu 12.04':'icycloud/ubuntu-baseimage:0.9.18',
	}
	if osname not in namedic:
		print osname
		print 'osname not in namedic'
		return
	imgname = namedic[osname]
	cli = Client(base_url='unix://var/run/docker.sock')
	container = cli.create_container(imgname,environment={'ROOT_PASS':password})
	cli.start(container)
	containerid = container['Id']
	print 'dockerid:',containerid
	imginfo = cli.inspect_container(containerid)
	imgip = imginfo['NetworkSettings']['IPAddress']
	print 'imgip',imgip
	machineobj = Machine(machineip=imgip,user=user,dockerid=containerid,status='R')
	machineobj.save()

	# url routing
	url = username + '.cloud.sample.com'
	if Router.objects.filter(url=url):
		print 'url already routed'
		return 
	routeobj = Router(url=url,user=user,machineip=imgip)
	routeobj.save()
	print 'success'

	


