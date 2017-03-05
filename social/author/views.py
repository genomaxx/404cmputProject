from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/a/')
def index(request):
    return render(request, 'author/homepage.html')

@login_required
def post(request):
    # Only process the author's post if it is a POST request
    if (request.METHOD != "POST"):
        return HttpReponseRedirect('/')

