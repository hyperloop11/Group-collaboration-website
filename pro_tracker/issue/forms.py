from django import forms
from django.contrib.auth.models import User
from .models import Issue, Comment

class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields= ['title', 'content', 'priority', 'author', 'completed']

    # def __init__(self, *args, **kwargs):
    #     super(IssueUpdateForm, self).__init__(*args, **kwargs)
        
    #     self.fields['author'].queryset = User.objects.all().filter(active=True)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= ['author', 'issue', 'body']
        widgets = {
            'author': forms.HiddenInput(),
            'issue' : forms.HiddenInput(),
        }