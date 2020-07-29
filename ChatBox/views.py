from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from .models import Thread
def home(request):
    sent = User.objects.all()
    return render(request, 'ChatBox/chat_home.html', {'sent_users':sent})

def room(request, username):
    if User.objects.filter(username=username).exists():
        u2 = User.objects.get(username=username)
        u1 = request.user
        thread = Thread.objects.get_thread_or_create(user1=u1,user2=u2)
        if thread.is_valid:
            msgs = Thread.objects.get_all_chats(thread).order_by('id')
            return render(request, 'ChatBox/chat_room.html', {'u':username, 'msgs':msgs})
        else:
            return HttpResponseNotFound("Error: You cant text this person")
    return HttpResponseNotFound("Error: No such user found")