"""Demon List models."""

# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from users.models import Profile

# Utilities
import re

values_list_points = [
    250.00, 228.48, 210.06, 194.28, 180.78, 169.22, 159.32, 150.84, 143.58, 137.37,
    132.05, 127.50, 123.60, 120.26, 117.40, 114.96, 112.86, 111.07, 109.53, 108.22,
    106.84, 105.48, 104.13, 102.79, 101.47, 100.16, 98.87, 97.58, 96.31, 95.06,
    93.81, 92.58, 91.36, 90.15, 88.95, 86.73, 84.59, 82.52, 80.52, 78.60, 76.74,
    74.94, 73.21, 71.53, 69.92, 68.36, 66.86, 65.41, 64.00, 62.65, 61.35, 60.08,
    58.87, 57.69, 56.56, 55.20, 53.88, 52.59, 51.34, 50.12, 48.94, 47.79, 46.66,
    45.57, 44.51, 43.48, 42.47, 41.50, 40.54, 39.62, 38.72, 37.84, 36.99, 36.16,
    35.35, 34.56, 33.80, 33.06, 32.33, 31.63, 30.94, 30.28, 29.63, 29.00, 28.38,
    27.79, 27.20, 26.64, 26.09, 25.55, 25.03, 24.53, 24.03, 23.55, 23.09, 22.63,
    22.19, 21.76, 21.34, 20.93, 20.54, 20.15, 19.78, 19.41, 19.06, 18.71, 18.38,
    18.05, 17.73, 17.42, 17.12, 16.83, 16.54, 16.26, 15.99, 15.73, 15.48, 15.23,
    14.99, 14.75, 14.52, 14.30, 14.08, 13.87, 13.67, 13.47, 13.27, 13.08, 12.90,
    12.72, 12.55, 12.38, 12.21, 12.05, 11.89, 11.74, 11.59, 11.45, 11.31, 11.17,
    11.04, 10.91, 10.79, 10.67, 10.55, 10.43, 10.32, 10.21, 10.10
]

class Demon(models.Model):
    """Demon model."""

    level = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    verificator = models.CharField(max_length=255)
    position = models.IntegerField()
    list_points = models.FloatField(default=0)
    photo = models.ImageField(upload_to='demons/photos')
    verification_video_embed = models.CharField(max_length=500)
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
    def save(self, *args, **kwargs):
        if self.list_points:
            self.list_points = round(self.list_points, 2)
        super(Demon, self).save(*args, **kwargs)

class Record(models.Model):
    """Record model."""

    demon = models.ForeignKey(Demon, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    best_time = models.TimeField()
    video = models.CharField(max_length=500, blank=True, null=True)
    raw_footage = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    mod = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mod', blank=True, null=True)
    mod_notes = models.TextField(blank=True, null=True)
    
    accepted = models.BooleanField(blank=True, null=True)

    datetime_submit = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return record."""
        return '{}'.format(self.id)

    def video_platform(self):
        youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/.+')
        twitch_pattern = re.compile(r'(https?://)?(www\.)?twitch\.(tv|com)/.+')
        twitch_clips_pattern = re.compile(r'(https?://)?clips\.twitch\.tv/.+')
        facebook_pattern = re.compile(r'(https?://)?(www\.)?facebook\.(com)/.+')
        google_drive_pattern = re.compile(r'(https?://)?drive\.google\.com/.+')

        if youtube_pattern.match(self.video):
            return "YouTube"
        elif twitch_pattern.match(self.video):
            return "Twitch"
        elif twitch_clips_pattern.match(self.video):
            return "Twitch"
        elif facebook_pattern.match(self.video):
            return "Facebook"
        elif google_drive_pattern.match(self.video):
            return "Drive"
        else:
            return ""

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

class Update(models.Model):
    version = models.CharField(max_length=5)
    changes = models.TextField(blank=True, null=True)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        # Return version
        return self.version
