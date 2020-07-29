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

class Thread(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    UID = models.TextField(default="")
    objects = ThreadManager()
    # def save(self):
    #     mask = hashlib.sha256()
    #     string = self.user_one.username+self.user_two.username
    #     mask.update(string.encode())
    #     self.UID = mask.hexdigest()
    #     print(len(self.UID))
    #     super.save(self)
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, default=None, blank=True, null=True)
    text = models.TextField()