from asyncio.windows_events import NULL
from enum import auto
from pickle import TRUE
from pyexpat import model
from sqlite3 import Timestamp
from xml.etree.ElementTree import Comment
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class blog(models.Model):
    sno = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=1000)
    Description = models.TextField()
    Short_Description = models.CharField(max_length=200 , default="")
    Slug = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.Slug
# class userblog(models.Model):
#     sno=models.AutoField(primary_key=True)
#     Title=models.CharField(max_length=1000)
#     Description=models.TextField()
#     Short_Description=models.CharField(max_length=200,default="")
#     Slug=models.CharField(max_length=200)
#     Time=models.DateTimeField(auto_now_add=True)
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     def __str__(self) :
#         return self.Slug
class blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(blog,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    Timestamp = models.DateTimeField(default=now)
    def __str__(self) :
        return self.comment[0:13]+"... by "+ self.user.username
    
class contactuser(models.Model):
    Name = models.CharField(max_length=30) 
    Address=models.CharField(max_length=50)
    Description = models.CharField(max_length=30)
    Email=models.EmailField()
    Time=models.DateTimeField(auto_now_add=True)