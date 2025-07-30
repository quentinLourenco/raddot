from django.db import models
from django.utils import timezone

from user_manager.models import User
from social_app.utils.file_paths import get_subraddot_banner_path, get_subraddot_icon_path


class Subraddot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    banner = models.ImageField(upload_to=get_subraddot_banner_path, null=True, blank=True)
    icon = models.ImageField(upload_to=get_subraddot_icon_path, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_subraddots')
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(User, related_name='joined_subraddots', blank=True)

    def __str__(self):
        return self.name
