from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import DetailView
from django.utils.html import escape
from django.db.models import Q
from CommonMark import commonmark

from post.models import Post
from comment.models import Comment

# Create your views here.

class PostView(generic.DetailView):
    model = Post
    template_name = 'view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        content = escape(self.get_object().content)
        content = commonmark(content)
        context['content'] = content
        context['comment_list'] = self.get_comment_list()
        return context

    def get_comment_list(self):
        comments = Comment.objects.filter(
            Q(post=self.get_object().id)
        ).order_by('-publishDate')
        return comments
