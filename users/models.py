# Django
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    # Proxy model that extends the base data with other information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_channel = models.URLField(max_length=200, blank=True, null=True)
    discord = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    picture = models.ImageField(upload_to="users/pictures", blank=True, null=True)
    country = models.ForeignKey("Country", on_delete=models.CASCADE, blank=True, null=True)
    list_points = models.FloatField(default=0)

    followers = models.ManyToManyField('self', related_name='followings', blank=True, symmetrical=False)
    
    dark_mode = models.BooleanField(default=False)

    verified = models.BooleanField(blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return username
        return self.user.username
    def save(self, *args, **kwargs):
        self.list_points = round(self.list_points, 2)
        super(Profile, self).save(*args, **kwargs)

class Country(models.Model):
    country = models.CharField(max_length=150, blank=True)
    list_points = models.FloatField(max_length=200, blank=True, default=0)
    picture = models.FileField(upload_to="countries/pictures", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return country
        return self.country
    def save(self, *args, **kwargs):
        self.list_points = round(self.list_points, 2)
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Countries"