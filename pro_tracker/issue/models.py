from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms


class Issue(models.Model):
    PRIORITY_CHOICES= (
        ('high','high'),
        ('medium','medium'),
        ('low', 'low')
    )

    title=models.CharField(max_length=100)
    content=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)
    priority=models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})