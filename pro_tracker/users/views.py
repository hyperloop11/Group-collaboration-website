from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from issue.models import Issue
from django.http import JsonResponse
from datetime import date, timedelta

def register(request):
    if request.method== 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can log in now.')
            return redirect('issue-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form =ProfileUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)
        #instance used to populate field with existing data
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form =ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/update_profile.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def dashboard(request):
    high_posts=request.user.issue_set.filter(completed=False).filter(priority='high')[:4]
    medium_posts=request.user.issue_set.filter(completed=False).filter(priority='medium')[:4]
    low_posts=request.user.issue_set.filter(completed=False).filter(priority='low')[:4]

    context={
        'high_posts': high_posts,
        'medium_posts': medium_posts,
        'low_posts':low_posts, 
    }
    return render(request,'users/dashboard.html', context)

def result_data(request):
    issue = request.user.issue_set.all()
    num_high = issue.filter(priority='high').count()
    num_medium = issue.filter(priority='medium').count()
    num_low = issue.filter(priority='low').count()

    priority_data=[
        {'high': num_high},
        {'medium': num_medium},
        {'low': num_low},
    ]
    
    return JsonResponse(priority_data, safe=False)

def finished_data(request):
    date_today= date.today()
    date_old=date_today - timedelta(7)
    issue = request.user.issue_set.filter(date_created__date__gte=date_old, date_created__date__lte=date_today)
    unfinished= issue.filter(completed=False).count()
    finished = issue.filter(completed=True).count()

    finished=[
        {'unfinished': unfinished},
        {'finished': finished},
    ]
    return JsonResponse(finished, safe=False)




    
