from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django import forms
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.forms import ModelForm


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

# class UserForm(ModelForm):
#     class Meta:
#         fields= ['title', 'content', 'priority', 'author']

#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.fields['author'].queryset = User.objets.all().exclude(username=title.author.get(id=1))

class Comment(models.Model):
    issue= models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = MarkdownxField()
    date_added = models.DateTimeField(auto_now_add=True)

    def formatted_markdown(self):
        return markdownify(self.body)

    def __str__(self):
        return f'{self.issue.title}- {self.name}'