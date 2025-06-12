from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Instagram_User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=151)
    followers = models.PositiveIntegerField(null=True, blank=True)
    posts = models.PositiveIntegerField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='instagram/', null=True, blank=True)
    password = models.CharField(max_length=128, blank=True, null=True)  # Add this line


    def __str__(self):
        return self.username
