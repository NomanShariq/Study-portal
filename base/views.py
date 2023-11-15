from django.shortcuts import render

# Create your views here.

rooms = [
    {'id' : 1 , 'name' : 'Lets learn Python!!'},
    {'id' : 2 , 'name' : 'Web dvelopers'},
    {'id' : 3 , 'name' : 'Logo designers needed'}
]

def homepage(request):
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request,pk): 
    room = None
    
    for i in rooms:
        if i['id'] == int(pk):
            room = i
            
    context = {'rooms':room}
    return render(request,'base/room.html',context)