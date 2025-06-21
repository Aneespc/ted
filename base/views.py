from django.shortcuts import render
from django.http import HttpResponse

from .models import Room

# Create your views here.

# rooms=[
#     {'id':1,'name':"python"},
#     {'id':2,'name':"design"},
#     {'id':3,'name':"developing"},
# ]

def home(request):
    rooms=Room.objects.all()
    context={"rooma":rooms}
    return render(request, 'base/home.html',context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    context={"room":room}
    return render(request, 'base/room.html',context)
