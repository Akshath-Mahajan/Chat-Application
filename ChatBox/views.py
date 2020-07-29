from django.shortcuts import render

def home(request):
    return render(request, 'ChatBox/chat_room.html')