from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Issue(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)
    priority=models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title