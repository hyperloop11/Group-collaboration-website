from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue

def home(request):
    context = {
        'posts': Issue.objects.all()
    }
    return render(request, 'issue/home.html', context)