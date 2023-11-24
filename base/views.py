from django.shortcuts import redirect, render
from base.form import Roomform

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

def createRoom(request):
    form = Roomform()
    if request.method == 'POST':
        form = Roomform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html',context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    
    if request.method == 'POST':
        form = Roomform(request.POST, instance=room)
        if form.is_valid():
           form.save()
           return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteForm(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'obj':room})