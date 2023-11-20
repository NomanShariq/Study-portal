from django.shortcuts import render

from base.models import Room

# Create your views here.

# rooms = [
#     {'id' : 1 , 'name' : 'Lets learn Python!!'},
#     {'id' : 2 , 'name' : 'Web dvelopers'},
#     {'id' : 3 , 'name' : 'Logo designers needed'}
# ]

def homepage(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request,pk): 
    room = Room.objects.get(id=pk)        
    context = {'rooms':room}
    return render(request,'base/room.html',context)