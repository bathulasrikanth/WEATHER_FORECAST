
from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    city = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cities = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"