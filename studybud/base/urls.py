from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('room/<str:pk>',views.room,name="room"),
    path('profile/<str:pk>',views.profile,name="user-profile"),
    
    path('create_room/',views.create_room,name="new_room"),
    path('update_room/<str:pk>',views.update_room,name="update_room"),
    path('delete_room/<str:pk>',views.delete_room,name="delete_room"),
    
    path('delete_msg/<str:pk>',views.delete_msg,name="delete_msg"),
    
    path('update_user/',views.update_user,name="update_user"),
    
    
    path('login/',views.login_page,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerUser,name="register"),
    
    path('topic_page/',views.topic_page,name="topics"),
    path('activity_page/',views.activity,name="activity")
]
