# Generated by Django 5.0 on 2023-12-24 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demonlist', '0012_record_mod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demon',
            name='min_percentage',
        ),
        migrations.RemoveField(
            model_name='demon',
            name='score_min',
        ),
    ]
