from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Issue
from django.contrib.auth.models import User, Permission

def home(request):
    context = {
        'posts': Issue.objects.all()
    }
    return render(request, 'issue/home.html', context)

class IssueListView(ListView):
    model = Issue
    template_name='issue/home.html'
    context_object_name='posts'

    #ORDERING
    def get_queryset(self):
        return Issue.objects.order_by('-id')

class IssueDetailView(DetailView):
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields= ['title', 'content', 'priority']

    def form_valid(self, form):
        form.save()
        form.instance.author.add(self.request.user)
        return super().form_valid(form)

    def view_type(self):
        return "Create"


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields= ['title', 'content', 'priority', 'author']
    #form_class=UserForm

    # def __init__(self, *args, **kwargs):
    #     super(IssueUpdateView, self).__init__(*args, **kwargs)
    #     self.fields['author'].queryset = User.objects.exclude(username=)
    
    def form_valid(self, form):
        form.save()
        form.instance.author.add(self.request.user)
        return super().form_valid(form)

    def test_func(self):
        post= self.get_object()
        if self.request.user in post.author.all() or self.request.user.has_perm('issue.change_issue'):
            return True
        else:
            return False

    def view_type(self):
        return "Update"

#to fix kwargs in issue list view, better not inherit from listView and make a function.

def UserIssue(request,username):
    #user = get_object_or_404( User,User.objects.get(username=username))
    user = User.objects.get(username=username)
    context = {
        'user': user,
        'posts': user.issue_set.all().order_by('-id')
    }
    return render(request, 'issue/user_issues.html', context)
