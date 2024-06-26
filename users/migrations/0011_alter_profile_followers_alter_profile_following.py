# Generated by Django 5.0 on 2023-12-25 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_followers_profile_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, to='users.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, to='users.profile'),
        ),
    ]
