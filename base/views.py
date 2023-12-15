from django.shortcuts import redirect, render
from base.form import Roomform, UserForm
from django.db.models import Q
from django.http import HttpResponse
from base.models import Message, Room, Topic
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# rooms = [
#     {'id' : 1 , 'name' : 'Lets learn Python!!'},
#     {'id' : 2 , 'name' : 'Web dvelopers'},
#     {'id' : 3 , 'name' : 'Logo designers needed'}
# ]

#   Login function
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username),
        except:
            messages.error(request, "User Does'nt exist.")
            
        user = authenticate(request , username=username,password=password)
        
        
        if user is not None:
            login(request,user)
            messages.success(request, "You have successfully logged in.")  # Add a success message
            return redirect('home')
        else:
            messages.error(request, "Username or password doesnt exist.")    
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

#   Logout function
def logoutUser(request):
    logout(request)
    return redirect('login')

#   Register function
def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "There is something Error occured during registation!!!.")    
    return render(request, 'base/login_register.html', {'form':form})

#   Index function
def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)  
    )
    rooms_list = Room.objects.all()
    # Pagination logic
    items_per_page = 6  # Show only 6 rooms per page
    paginator = Paginator(rooms_list, items_per_page)
    page = request.GET.get('page')

    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
        
    topic = Topic.objects.all()
    room_count = rooms_list.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms' : rooms , 'topic':topic , 'room_count': room_count , 'room_messages' : room_messages}
    return render(request, 'base/home.html', context)

#   User Profile function
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()
    context = {'user':user , 'rooms' : room , 'topic' : topic , 'room_messages' : room_messages}
    return render(request, 'base/profile.html', context) 

#   Edit User function
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-Profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form' : form})

#   ALL Room function
def room(request,pk): 
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )   
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'rooms':room, 'room_messages' : room_messages , 'participants' : participants}
    return render(request,'base/room.html',context)

#   Create Room function
@login_required(login_url="login")
def createRoom(request):
    form = Roomform()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_created = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_created)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')
    
    context = {'form': form, 'topic' : topics}
    return render(request, 'base/room_form.html',context)

#   Update Room function
@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        topic_created = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_created)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form,  'topic' : topics}
    return render(request, 'base/room_form.html', context)

#   Delete Room function
@login_required(login_url="login")
def deleteForm(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
            return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'message':room})

#   Edit Msg function
@login_required(login_url="login")
def editMsg(request, pk):
    editmsg= Message.objects.get(id=pk)
    form = Roomform(instance=editmsg)
        
    if request.method == 'POST':
        editmsg = Roomform(request.POST, instance=editmsg)
        if form.is_valid():
           form.save()
           return redirect('home')
    
    if request.user != editmsg.user:
            return HttpResponse("You are not allowed here!!")
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

#   Delete Msg function
@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete_form.html', {'message' : message})

