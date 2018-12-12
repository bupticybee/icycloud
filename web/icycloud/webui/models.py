from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CloudUser(models.Model):
    user = models.OneToOneField(User)
    maxmachine = models.IntegerField(default=1)

class Machine(models.Model):
    MAYBECHOICE = (
        ('C', 'Creating'),
        ('R', 'Running'),
        ('D', 'Down'),
        ('F', 'Failed'),
    )
    machineip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    dockerid = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=1,choices=MAYBECHOICE,default='C',null=False,blank=False)

class InviteCode(models.Model):
    code = models.CharField(max_length=20,primary_key=True,verbose_name='InvitieCode')
    used = models.BooleanField(null=False,default=False,verbose_name='Used')

    class Mate:
        verbose_name_plural='InviteCode'
        verbose_name='Invite'


class Router(models.Model):
    url = models.CharField(max_length=255,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    machineip = models.GenericIPAddressField(null=True)
