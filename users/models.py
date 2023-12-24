# Django
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    # Proxy model that extends the base data with other information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_channel = models.URLField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=50, blank=True)
    list_points = models.FloatField(blank=True)

    picture = models.ImageField(upload_to="users/pictures", blank=True, null=True)

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