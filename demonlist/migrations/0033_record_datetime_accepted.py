# Generated by Django 4.2.7 on 2024-01-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demonlist', '0032_record_top_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='datetime_accepted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
