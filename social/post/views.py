from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def post_view(request, pk):
    return HttpResponse("Hello!" + str(pk))
