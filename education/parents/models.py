#-*- encoding=utf-8 -*-

from django.db import models
from django.template.defaultfilters import default

from users.models import User

# Create your models here.

'''
class Users(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    privilege = models.PositiveSmallIntegerField(default=3)
    audited = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.username
'''

class Parents(models.Model):
    username = models.CharField(primary_key=True, max_length=20)  
    name = models.CharField(max_length=4, null=True,blank=True)
    balance = models.PositiveIntegerField(default=0, null=True,blank=True)
    child_name = models.CharField(max_length=10, null=True,blank=True)
    child_age = models.IntegerField(default=10, null=True,blank=True)
    child_sex = models.CharField(max_length=6, null=True,blank=True)
    
    def __unicode__(self):
        return self.username
    
    
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)  
    starts = models.PositiveSmallIntegerField(default=5)
    words = models.CharField(max_length=50)
