from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User 
from .models import project,Topic,Message
from .forms import Project_form,UserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

rooms=[
    
    
    
        {'id':1,'name':'UNITY'},
        {'id':2,'name':'UNREAL'},
        {'id':3,'name':'MACHINE LEARNING'},
        {'id':4,'name':'DEEP SPACE NETWORK'},
    ]
r1=['GTA 5','Red dead Redemption ','bully','L.A.Noir','MidNight club']

def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User doesn't exists")
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or password is incorrect")
                    
                 
            
    context={'page':page}
    return render(request,'base/login.html',context=context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page='register'
    form=UserCreationForm()
    
    #process the form
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)# data cleaning so it is not saved(committed)
            user.username=user.username.lower()
            user.save()
            #login the user now
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error has occured")
            
    
    return render(request,'base/login.html',{'form':form})    

# Create your views here.
def home(Request):
    q=Request.GET.get('q') if Request.GET.get('q')!= None else ''
    print(q)
    #rooms=project.objects.all()
    rooms=project.objects.filter(Q(topic__name__icontains=q)|
                                 Q(name__icontains=q)|
                                 Q(description__icontains=q))
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(Project__name__icontains=q))
    topics=Topic.objects.all()[0:4]
    print(topics)
    cdata={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}#key is used in the HTML "rooms"
    #cdata1={'RockstarGames':r1}
    return render(Request,'base/home.html',cdata)

def room(request,pk):
    '''room_name=None
    for i in rooms:
        if i['id']==int(pk):
            room_name=i
    #form a context and send it 
    cdata={'room':room_name}    '''
    room_name=project.objects.get(id=pk)
    room_messages=room_name.message_set.all().order_by("-created") # type: ignore
    participants=room_name.participants.all()
    
    if request.method=="POST":
        msg=Message.objects.create(
            user=request.user,
            Project=room_name,
            body=request.POST.get('body')
        )
        room_name.participants.add(request.user)
        #room_name.save()
        return redirect('room',pk=room_name.id)
    
    cdata={'room':room_name,'room_messages':room_messages,'participants':participants}
    
    return render(request,'base/room.html',cdata)
 
def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=project.objects.filter(host=user)
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    print(rooms)
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form=Project_form()
    topics=Topic.objects.all()
    if request.method=='POST':
        #get the topic
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        project.objects.create(
            host=request.user,
            topic=topic,
            description=request.POST.get('description'),
            name=request.POST.get('name')
        )
        
        '''form1=Project_form(request.POST)#adds new room
        if form1.is_valid:
            room=form1.save(commit=False)#this gives the instance of the class
            room.host=request.user #setting up the host name 
            room.save()'''
        return redirect('home')
        
    cdata={'form':form,'topics':topics}
    return render(request,'base/room_form.html',cdata)

@login_required(login_url='login')
def update_room(request,pk):#to know what room we are updating 
        room=project.objects.get(id=pk)
        forms=Project_form(instance=room)
        topics=Topic.objects.all()
        
        #only the creator of the room should be able to modify
        if request.user!=room.host:
            return HttpResponse('Restricted!!')
        
        
        if request.method=='POST':
            #form=Project_form(request.POST,instance=room)#instance will replace the existing room
            #if form.is_valid:
            #    form.save()
            topic_name=request.POST.get('topic')
            topic,created=Topic.objects.get_or_create(name=topic_name)
            
            room.name=request.POST.get('name')
            room.description=request.POST.get('description')
            room.topic=topic
            room.save()
            
            return redirect('home')
        cdata={'form':forms,'topics':topics,'room':room}
        return render(request,'base/room_form.html',cdata)
    
@login_required(login_url='login')    
def delete_room(request,pk):
    room=project.objects.get(id=pk)
    
    #only the creator of the room should be able to modify
    if request.user!=room.host:
            return HttpResponse('Restricted!!')
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/confirmDelete.html',{'rooms':room})        

@login_required(login_url='login')    
def delete_msg(request,pk):
    msg=Message.objects.get(id=pk)
    
    #only the creator of the room should be able to modify
    if request.user!=msg.user:
            return HttpResponse('Restricted!!')
    
    if request.method=='POST':
        msg.delete()
        return redirect('home')
    return render(request,'base/confirmDelete.html',{'rooms':msg})    

@login_required(login_url='login')    
def update_user(request):
    user=request.user
    form=UserForm(instance=user)
    
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile',pk=user.id)
    
    return render(request,'base/update-user.html',{'form':form})

def topic_page(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    topics=Topic.objects.filter(Q(name__icontains=q))
    
    return render(request,"base/topics.html",{'topics':topics})

def activity(request):
    
    room_messages=Message.objects.all()
    
    
    return render(request,"base/activity.html",{'room_messages':room_messages})
