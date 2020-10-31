from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Issue
from django.contrib.auth.models import User, Permission
from .forms import IssueUpdateForm, CommentForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.signals import notify

def home(request):
    context = {
        'posts': Issue.objects.all()
    }
    return render(request, 'issue/home.html', context)

class IssueListView(ListView):
    model = Issue
    template_name='issue/home.html'
    context_object_name='posts'
    paginate_by=6

    #ORDERING
    def get_queryset(self):
        return Issue.objects.filter(completed=False).order_by('-id')

class OldIssueListView(ListView):
    model = Issue
    template_name='issue/home.html'
    context_object_name='posts'
    paginate_by=6

    #ORDERING
    def get_queryset(self):
        return Issue.objects.filter(completed=True).order_by('-id')

class IssueDetailView(FormMixin, DetailView):
    model = Issue
    form_class=CommentForm

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'issue': self.object.id, 'author': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            curr_issue = Issue.objects.get(pk=self.object.id)
            for user in curr_issue.author.all() :
                if self.request.user != user:
                    notify.send(
                            request.user,
                            recipient=user,
                            verb = 'commented on your issue',
                            target=curr_issue,
                        )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(IssueDetailView, self).form_valid(form)



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
    form_class = IssueUpdateForm
    # leader =self.get_object().author.first()
    # #author = forms.ModelChoiceField(queryset=User.objects.exclude(leader))
    
    # form_class.fields['author'].queryset=User.objects.exclude(leader)
    #form_class=UserForm

    # def __init__(self, *args):
    #     super(IssueUpdateView, self).__init__(*args)
    #     leader =self.get_object().author.first()
    #     self.fields['author'].queryset = User.objects.exclude(leader)
    
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
    this_user = get_object_or_404(User, username=username)

    posts = this_user.issue_set.filter(completed=False).order_by('-id')
    paginator = Paginator(posts, 2) # Show 4 blogs per page.

    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'this_user': this_user,
        #'posts': this_user.issue_set.all().order_by('-id'),
        'posts': page_obj,
    }
    return render(request, 'issue/user_issues.html', context)

def UserIssueArchives(request,username):
    this_user = get_object_or_404(User, username=username)

    posts = this_user.issue_set.filter(completed=True).order_by('-id')
    paginator = Paginator(posts, 2) # Show 4 blogs per page.

    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'this_user': this_user,
        #'posts': this_user.issue_set.all().order_by('-id'),
        'posts': page_obj,
    }
    return render(request, 'issue/user_issues.html', context)