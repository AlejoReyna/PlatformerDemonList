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
    list_points = models.FloatField()
    photo = models.ImageField(upload_to='demons/photos')
    verification_video = models.CharField(max_length=500)

    level_id = models.BigIntegerField(blank=True, null=True)
    object_count = models.BigIntegerField(blank=True, null=True)
    demon_difficulty = models.CharField(max_length=50, blank=True, null=True)
    update_created = models.CharField(max_length=5, blank=True, null=True)
    level_password = models.BigIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return level."""
        return '{}'.format(self.level)

class Record(models.Model):
    """Record model."""

    demon = models.ForeignKey(Demon, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    video = models.CharField(max_length=500)
    raw_footage = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)
    mod = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mod', blank=True, null=True)
    mod_notes = models.TextField(blank=True, null=True)
    
    accepted = models.BooleanField(blank=True, null=True)

    datetime_submit = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return record."""
        return '{}'.format(self.id)

class Changelog(models.Model):
    """Changelog model."""

    demon = models.ForeignKey(Demon, on_delete=models.CASCADE)
    reason = models.CharField(max_length=500)
    position = models.IntegerField()
    change_number = models.IntegerField(blank=True, null=True)
    change_type_options = (("Up", "Up"),
                           ("Down", "Down"))
    change_type = models.CharField(max_length=500, choices=change_type_options, blank=True, null=True)

    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return changelog."""
        return '{}'.format(self.id)

