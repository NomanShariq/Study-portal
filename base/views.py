from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'home.html')

def room(request): 
    return render(request,'room.html')