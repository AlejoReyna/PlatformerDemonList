# Generated by Django 5.0 on 2023-12-25 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_profile_following_alter_profile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
    ]