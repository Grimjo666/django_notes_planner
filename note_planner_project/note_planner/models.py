from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from transliterate import translit


class TaskColorSettings(models.Model):
    high_priority_color = models.CharField(max_length=20, default='#440673')
    medium_priority_color = models.CharField(max_length=20, default='#06734b')
    low_priority_color = models.CharField(max_length=20, default='#383838')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class UserProfilePhoto(models.Model):
    photo = models.FileField(upload_to='user_profile_photos')
    main_photo = models.BooleanField(default=False)
    load_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
