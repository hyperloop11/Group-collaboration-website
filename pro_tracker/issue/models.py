from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Issue(models.Model):
    PRIORITY_CHOICES= (
        ('high','high'),
        ('medium','medium'),
        ('low', 'low')
    )

    title=models.CharField(max_length=100)
    content= MarkdownxField()
    date_created=models.DateTimeField(default=timezone.now)
    priority=models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    author = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})

    def formatted_markdown(self):
        return markdownify(self.content)

    def body_summary(self):
        return markdownify(self.content[:200] + "...")