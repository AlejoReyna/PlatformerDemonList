# Django
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    # Proxy model that extends the base data with other information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_channel = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    picture = models.ImageField(upload_to="users/pictures", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    list_points = models.FloatField(default=0)

    followers = models.ManyToManyField('self', related_name='followings', blank=True, symmetrical=False)
    
    dark_mode = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return username
        return self.user.username
    
class Country(models.Model):
    country = models.CharField(max_length=150, blank=True)
    list_points = models.FloatField(max_length=200, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return country
        return self.country
    
    class Meta:
        verbose_name_plural = "Countries"