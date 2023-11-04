# Generated by Django 4.2.6 on 2023-11-03 17:01

import App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_remove_profilepictures_cover_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pictures',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.FileField(default=None, storage=App.models.OverwriteStorage(), upload_to='ProfilePictures/'),
        ),
        migrations.DeleteModel(
            name='ProfilePictures',
        ),
    ]