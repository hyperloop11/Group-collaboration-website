from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from issue.models import Issue


class CommentNoticeListView(LoginRequiredMixin, ListView):
    '''notification list'''
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    # login_url = '/userprofile/login/'

    #Query set for unread notifications
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    '''update notification status'''
    #Processing get requests
    def get(self, request):
        #Get unread message
        notice_id = request.GET.get('notice_id')
        #Update single notice
        if notice_id:
            issue = Issue.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(issue)
        #Update all notifications
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')