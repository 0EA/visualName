from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    draft_right_left = models.IntegerField(default=5)

    def __str__(self):
        return self.user.username
    