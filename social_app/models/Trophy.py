from django.db import models
from user_manager.models import User
from social_app.models.Subraddot import Subraddot


class Trophy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trophies')
    subraddot = models.ForeignKey(Subraddot, on_delete=models.CASCADE, null=True, related_name='trophies')
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='trophy_icons/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username} ({self.subraddot.name})"
