from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #Notification list
    path('list/', views.CommentNoticeListView.as_view(), name='list'),
    #Update notification status
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
]