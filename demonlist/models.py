"""Demon List models."""

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from users.models import Profile

class Demon(models.Model):
    """Demon model."""

    level = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    verificator = models.CharField(max_length=255)
    position = models.IntegerField()
    min_percentage = models.IntegerField()
    score_complete = models.FloatField()
    score_min = models.FloatField()
    photo = models.ImageField(upload_to='demons/photos')
    verification_video = models.CharField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return level."""
        return '{}'.format(self.level)

class Record(models.Model):
    """Record model."""

    demon = models.ForeignKey(Demon, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    percentage = models.IntegerField()
    video = models.CharField(max_length=500)
    raw_footage = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)
    
    accepted = models.BooleanField(blank=True, null=True)

    datetime_submit = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return record."""
        return '{}'.format(self.id)
