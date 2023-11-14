from django.urls import path

from . import views


urlpatterns = [
    path('' , views.homepage , name = 'Home'),
    path('room/<str:pk>/' , views.room , name = 'Room'),
]