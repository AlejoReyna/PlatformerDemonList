# Generated by Django 5.0 on 2023-12-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demonlist', '0005_rename_datetime_accepted_record_datetime_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='demon',
            name='verification_video',
            field=models.CharField(default='ol', max_length=500),
            preserve_default=False,
        ),
    ]