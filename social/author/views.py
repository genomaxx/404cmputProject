from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from author.models import Author
from post.models import Post
from django.db.models import Q
import sys
# Create your views here.

@login_required(login_url='/a/')
def index(request):
    # This page displays the author's stream/post feed.
    # https://docs.djangoproject.com/en/1.10/topics/db/queries/
    authorContext = Author.objects.get(id=request.user)
    # Get all post objects that are public and private
    # TODO: Add to the query to expand the feed.
    try:
        posts = Post.objects.filter(
            Q(privacyLevel=0) | 
            (Q(privacyLevel=4) & Q(author__id=authorContext.id))
            ).order_by('-publishDate')
    except:
        return HttpResponse(sys.exc_info[0])
    
    try:
       if (len(posts) > 0):
           context = {'posts': posts}
           return render(request, 'author/index.html', context)
    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/index.html')

@login_required(login_url='/author_post/')
def author_post(request):
    # Only process the author's post if it is a POST request
    if (request.method != 'POST'):
        return HttpReponseRedirect('/a/')

    if (request.POST['post_content'] == None):
        return

    try:
        # Get the logged in user and the associated author object.
        #userContext = User.objects.get(username=request.user.username)
        post_body = request.POST['post_content']
        authorContext = Author.objects.get(id=request.user)

        # Create and save a new post.
        newPost = Post(author=authorContext, 
                       content=request.POST['post_content'], 
                       privacyLevel=request.POST['privacy_level'])
        newPost.save()
    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/a/')

@login_required(login_url='/profile/')
def profile(request):
    # This page displays the author's profile.
    # https://docs.dj# This page displays the author's profile.angoproject.com/en/1.10/topics/db/queries/
    authorContext = Author.objects.get(id=request.user)

    # TODO: Add to the query to expand the feed.
    try:
        posts = Post.objects.filter(
            Q(author__id=authorContext.id)
            ).order_by('-publishDate')
    except:
        return HttpResponse(sys.exc_info[0])
    
    try:
       if (len(posts) > 0):
           context = {'posts': posts}
           return render(request, 'author/profile.html', context)
    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/profile.html')

@login_required(login_url='/edit/')
def edit(request):
    return render(request, 'author/edit.html')


@login_required(login_url='/edit_post/')
def edit_post(request):
    # Only process the author's post if it is a POST request
    if (request.method != 'POST'):
        return HttpReponseRedirect('/edit/')

    try:

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        gitURL = request.POST['gitURL']
        authorContext = Author.objects.get(id=request.user)

        # save author.
        authorContext.id.firstname = firstname
        authorContext.id.lastname = lastname
        authorContext.phone = phone
        authorContext.dob = dob
        authorContext.gender = gender
        authorContext.gitURL = gitURL

        authorContext.save()


    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/a/profile/')
