# Generated by Django 4.2.6 on 2023-12-04 13:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('note_planner', '0018_rename_maid_photo_userprofileinfo_main_photo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileInfo',
            new_name='UserProfilePhoto',
        ),
    ]