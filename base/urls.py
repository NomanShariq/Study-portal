from django.urls import path

from . import views


urlpatterns = [
    path('' , views.homepage , name = 'home'),
    path('room/<str:pk>/' , views.room , name = 'room'),
    path('update-form/<str:pk>', views.updateRoom , name='update-room'),
    path('delete-form/<str:pk>', views.deleteForm , name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage , name='delete-message'),
    path('create-form/', views.createRoom , name='create-room'),
    path('login/', views.loginPage , name='login'),
    path('register/', views.registerPage , name='register'),
    path('logout/', views.logoutUser , name='logout'),
]