# Generated by Django 4.2.7 on 2023-12-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_country_list_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='countries/pictures'),
        ),
    ]