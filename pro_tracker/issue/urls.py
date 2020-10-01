from django.urls import path
from .views import (
    IssueListView, IssueDetailView, 
    IssueCreateView, IssueUpdateView
)
from . import views

urlpatterns = [
    path('', views.IssueListView.as_view(), name='issue-home'),
    path('<int:pk>/', views.IssueDetailView.as_view(), name='issue-detail'),
    path('<int:pk>/update', views.IssueUpdateView.as_view(), name='issue-update'),
    path('new/', views.IssueCreateView.as_view(), name='issue-create'),
]
