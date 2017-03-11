from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def add(request, post):
    return HttpResponseRedirect('/post/' + post.id)
