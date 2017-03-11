from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from author.models import Author
import sys

#Create your views here

# The homee page for registration and login.
def index(request):
    return render(request, 'login/index.html')

# Register a user
def register(request):
    # Only process the registration if it is a POST request
    if (request.method != 'POST'):
        return HttpResponseRedirect('/')
    
    regForm = forms.RegistrationForm(request.POST)
    
    # Check if the form is valid
    if (not regForm.is_valid()):
        return HttpResponse('<h1>Form not valid</h1>')

    # Create and save the User and Author model.
    # Both need to be saved because there is no point of saving one with out the other since
    # they are in a one-to-one relationship.
    try:
        user = regForm.save() # Save the form data
        # Ref: http://stackoverflow.com/questions/2936276/django-modelforms-user-and-userprofile-not-hashing-password
        user.set_password(user.password) # Set the password
        user.is_active = True
        user.save() # Push to db
        userEmail = request.POST['email']
        newUser = User.objects.get(email=userEmail)

        # Create and save the Author model
        author = Author(id=newUser)
        author.save()
    except:
        return HttpResponse(sys.exc_info[0]) #TODO: Will need to change this to a nicer UI later

    return HttpResponseRedirect('/') #TODO: Will need to change the page that gets returned

# User login
def login(request):
    # Only process the login if it is a POST request
    if (request.method != 'POST'):
        return HttpResponseRedirect('/')

    email = request.POST['user']
    password = request.POST['password']

    # Get the user. Doubles as making sure the user exists.
    try:
        logInUser = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse('<h1>This email does not exist</h1>') #TODO: Make this pretty

    author = authenticate(username=logInUser.username, password=password)
    if author is not None:
        django_login(request, author)
        return redirect('/author/')
    
    return HttpResponse('<h1>Wrong password :(</h1>')

@login_required()
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
