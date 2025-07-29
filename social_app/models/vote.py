from django.db import models
from django.utils import timezone

from user_manager.models import User
from .post import Post

class VotePost(models.Model):
    VOTE_VALUES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_VALUES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')  # Empêche un utilisateur de voter plusieurs fois sur le même post

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.post.title}"
