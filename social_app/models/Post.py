from django.db import models
from django.utils import timezone

from user_manager.models import User
from .Subraddot import Subraddot
from social_app.utils.file_paths import get_post_image_path


class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )

    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to=get_post_image_path, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    subraddot = models.ForeignKey(Subraddot, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
