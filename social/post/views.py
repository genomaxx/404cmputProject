from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from post.models import Post

# Create your views here.

class PostView(generic.DetailView):
    model = Post
    template_name = 'view.html'

# def post_view(request, pk):
#     return HttpResponse("Hello!" + str(pk))
