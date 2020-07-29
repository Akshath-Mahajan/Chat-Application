from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import hashlib
class ThreadManager(models.Manager):
    def get_thread_or_create(self, user1, user2):
        Q1 = Q(user_one=user1)&Q(user_two=user2)
        Q2 = Q(user_one=user2)&Q(user_two=user1)
        BaseQ = Q1|Q2
        qs = Thread.objects.filter(BaseQ)
        if qs.exists():
            return qs[0]
        else:
            new_obj = Thread(user_one=user1, user_two=user2)
            new_obj.save()
            return new_obj
    def get_all_chats(self, thread):
        return ChatMessage.objects.filter(thread=thread)
class Thread(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    UID = models.TextField(default="")
    is_valid = models.BooleanField(default=True)
    objects = ThreadManager()
    #def save(self):
    # if any users are blocked then turn isvalid to false
    # if user1 not related to user2 and openmessging is false then turn isvalid to false
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField()