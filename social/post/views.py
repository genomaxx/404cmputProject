from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import DetailView
from django.utils.html import escape
from CommonMark import commonmark

from post.models import Post

# Create your views here.

class PostView(generic.DetailView):
    model = Post
    template_name = 'view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        content = escape(context['post'].content)
        content = commonmark(content)
        context['content'] = content
        return context
