from django.db import models
from django.utils import timezone

from user_manager.models import User


class Subreddit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    banner = models.ImageField(upload_to='subreddit/banners/', null=True, blank=True)
    icon = models.ImageField(upload_to='subreddit/icons/', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_subreddits')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
