from django.forms import ModelForm 
from .models import Room , User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class Roomform(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','avatar','username','email','bio']