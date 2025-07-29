from django.db import models
from django.utils import timezone

from user_manager.models import User
from .Subraddot import Subraddot

class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('link', 'Link'),
    )

    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    subraddot = models.ForeignKey(Subraddot, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
