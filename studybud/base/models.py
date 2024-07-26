from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):#this will be displayed in the admin console
         return self.name

class project(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    update=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :#this will be displayed in the admin console
        return self.name
    
class Message(models.Model):
        Project=models.ForeignKey(project,on_delete=models.CASCADE)
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        body=models.TextField()
        update=models.DateTimeField(auto_now=True)
        created=models.DateTimeField(auto_now_add=True)
        
        
        
        def __str__(self):#this will be displayed in the admin console
             return self.body[:50]
