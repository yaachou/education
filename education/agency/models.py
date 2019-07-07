from django.db import models as db_models
from users.models import User
from django.forms import *

# Create your db_models here.
class ApplyForm_a( db_models.Model ):
    username = db_models.CharField( max_length=20 ,primary_key=True )  ##username varchar(30) not null,
    field = db_models.CharField( max_length=100 )    ##field varchar(100) not null,
    idcode = db_models.CharField( max_length=30 )    ##idcode varchar(30) not null,
    address = db_models.CharField( max_length=100 , null=True  )  ##address varchar(100) ,  
    aim_age = db_models.CharField(max_length=10) 
    email = db_models.EmailField()    
    phone = db_models.CharField( max_length=13 )
    intro = db_models.CharField(max_length=200)
    class Meta:
        app_label='agency'
        
class ApplyForm_t( db_models.Model ):
    username = db_models.CharField( max_length=20 ,primary_key=True )  ##username varchar(30) not null,
    name = db_models.CharField( max_length=30 )    ##field varchar(30) not null,
    sex = db_models.CharField( max_length=1 )      ##
    age =db_models.PositiveSmallIntegerField()    ##
    field = db_models.CharField( max_length=100 )    ##field varchar(100) not null,
    aim_age = db_models.CharField(max_length=10) 
    email = db_models.EmailField()      
    phone = db_models.CharField( max_length=13 )
    idcard = db_models.CharField(max_length=18)
    intro = db_models.CharField(max_length=200)
    class Meta:
        app_label='agency'
    
class Lessons( db_models.Model ):
    lesson_id=db_models.AutoField(primary_key=True)
    cname= db_models.CharField(max_length=100)
    cprice = db_models.PositiveIntegerField()
    cstarttime = db_models.DateField()
    cendtime = db_models.DateField()
    caim_age=db_models.CharField(max_length=1,null=True)
    carea = db_models.CharField(max_length=20)
    cteacher = db_models.CharField(max_length=20)
    cfield = db_models.CharField( max_length=100 )
    ccontend = db_models.TextField( null=True )
    chomework = db_models.TextField( null=True)
    lesson_user = db_models.CharField(max_length=20,null=True,blank=True)
    class Meta:
        app_label='agency'


class ListenApply( db_models.Model):
    apply_id=db_models.AutoField(primary_key=True)
    lesson_id=db_models.ForeignKey(Lessons,on_delete=db_models.CASCADE)
    username = db_models.CharField( max_length=20  )  ##username varchar(30) not null,
    cname = db_models.CharField(max_length=100,default="")
    accepted=db_models.BooleanField(default=False)

#公告板
class Notice( db_models.Model ):
    notice_id = db_models.AutoField(primary_key=True) 
    notice_time = db_models.TimeField(auto_now=True) 
    username = db_models.CharField( max_length=20  )  ##username varchar(30) not null,
    notice_title = db_models.CharField(max_length=20)
    notice_content = db_models.TextField(null=False)


