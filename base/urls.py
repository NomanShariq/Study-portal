from django.urls import path

from . import views


urlpatterns = [
    path('' , views.homepage , name = 'home'),
    path('room/<str:pk>/' , views.room , name = 'room'),
    path('update-form/<str:pk>', views.updateRoom , name='update-room'),
    path('delete-form/<str:pk>', views.deleteForm , name='delete-room'),
    path('create-form/', views.createRoom , name='create-room')
]