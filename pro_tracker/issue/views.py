from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Issue

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

class IssueCreateView(CreateView):
    model = Issue
    fields= ['title', 'content', 'priority']

    def form_valid(self, form):
        form.save()
        form.instance.author.add(self.request.user)
        return super().form_valid(form)