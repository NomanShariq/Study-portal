from django.shortcuts import redirect, render
from base.form import Roomform
from django.db.models import Q
from base.models import Room, Topic
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout

# Create your views here.

# rooms = [
#     {'id' : 1 , 'name' : 'Lets learn Python!!'},
#     {'id' : 2 , 'name' : 'Web dvelopers'},
#     {'id' : 3 , 'name' : 'Logo designers needed'}
# ]

def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username),
        except:
            messages.error(request, "User Does'nt exist.")
            
        user = authenticate(request , username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesnt exist.")    
        
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)  
    )
    topic = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms' : rooms , 'topic':topic , 'room_count': room_count}
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