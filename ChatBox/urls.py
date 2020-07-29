from django.urls import path, include
from .views import home, room
urlpatterns = [
    path('', home, name='chat_home'),
    path('<str:username>', room, name='chat_room'),
]