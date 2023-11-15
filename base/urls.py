from django.urls import path

from . import views


urlpatterns = [
    path('' , views.homepage , name = 'home'),
    path('room/<str:pk>/' , views.room , name = 'room'),
]