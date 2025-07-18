from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# rooms=[
#     {'id':1,'name':"python"},
#     {'id':2,'name':"design"},
#     {'id':3,'name':"developing"},
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or paasword incorrect')
    context={'page':page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

    context={}
    return render (request,'base/login_register.html',context)

def registerPage(request):
    page='register'
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')

    
    context={'form':form}
    return render (request,'base/login_register.html',context)



def home(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    rooms=Room.objects.filter(topic__name__icontains=q)
    topics =Topic.objects.all()

    room_count=rooms.count()
    context={"rooma":rooms,'topics':topics,'room_count':room_count}
    return render(request, 'base/home.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    context={"room":room}
    return render(request, 'base/room.html',context)


@login_required(login_url='logins')
def createRoom(request):
    form=RoomForm()
    if request.method =='POST':
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='logins')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form= RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse("Only room owner can update the room")

    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='logins')
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse("Only room owner can delete the room")
   
    if request.method =="POST":
       room.delete()
       return redirect('home')
    return render(request,'base/delete.html',{'obj':room}) 
