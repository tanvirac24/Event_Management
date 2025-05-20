
from events.models import Event
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(
        User, on_delete=models.CASCADE,related_name='userprofile',primary_key=True)
    profile_image=models.ImageField(upload_to='profile_images',blank=True)
    bio=models.TextField(blank=True)
    phone=models.CharField(max_length=12, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'
# Create your models here.
