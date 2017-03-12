from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from author.models import Author
from post.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from . import forms
import sys
import base64
import uuid
import re
# Create your views here.


@login_required(login_url='/author/')
def index(request):
    # This page displays the author's stream/post feed.
    # https://docs.djangoproject.com/en/1.10/topics/db/queries/
    author = Author.objects.get(id=request.user)
    context = {'author': author}
    # Get all post objects that are public and private
    # TODO: Add to the query to expand the feed.
    try:
        posts = Post.objects.all().order_by('-publishDate')
    except:
        return HttpResponse(sys.exc_info[0])

    try:
        if (len(posts) > 0):
            context['posts'] = posts
            return render(request, 'author/index.html', context)
    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/index.html', context)


@login_required(login_url='/author_post/')
def author_post(request):
    # Only process the author's post if it is a POST request
    if (request.method != 'POST'):
        return HttpResponseRedirect('/author/')

    if (request.POST['post_content'] is None):
        return

    try:
        # Get the logged in user and the associated author object.
        # userContext = User.objects.get(username=request.user.username)
        # post_body = request.POST['post_content']
        authorContext = Author.objects.get(id=request.user)

        if ('image' in request.FILES.keys()):
            # Create and save a new post.
            # encode image into base64 here and make nice image url too
            imgname = re.sub('[^._0-9a-zA-Z]+','',request.FILES['image'].name)
            newPost = Post(author=authorContext,
                           content=request.POST['post_content'],
                           privacyLevel=request.POST['privacy_level'], image = base64.b64encode(request.FILES['image'].read()),\
                           image_url = '{0}_{1}_{2}'.format(request.user, str(uuid.uuid4())[:8], imgname),\
                           image_type = request.FILES['image'].content_type)

        else:
            newPost = Post(author=authorContext,
               content=request.POST['post_content'],
               privacyLevel=request.POST['privacy_level'])
        newPost.save()
    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/author/')
    
# http://stackoverflow.com/questions/3539187/serve-static-files-through-a-view-in-django
@login_required()
def author_image(request,pk,pk1):
    post = get_object_or_404(Post, id=pk, image_url= pk1)
    response = HttpResponse(content=base64.b64decode(post.image), content_type=post.image_type)
    response['Content-Disposition'] = "filename="+post.image_url
    return response


def profile(request, id):
    # This page displays the author's profile.
    user = User.objects.get(id=id)
    author = Author.objects.get(id=user)
    context = {'author': author}

    try:
        posts = Post.objects.filter(
            Q(author__id=author.id)
            ).order_by('-publishDate')
    except:
        return HttpResponse(sys.exc_info[0])

    try:
       if (len(posts) > 0):
           context['posts'] = posts
    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/profile.html', context)

@login_required(login_url='/edit/')
def edit(request):
    authorContext = Author.objects.get(id=request.user)
    return render(request, 'author/edit.html', {'author':authorContext})



@login_required(login_url='/edit_post/')
def edit_post(request):
    # This page edits the author's profile

    if (request.method != 'POST'):
        return HttpReponseRedirect('/edit/')

    editForm = forms.EditForm(request.POST)


    if (not editForm.is_valid()):
        return HttpResponse('<h1>Form not valid</h1>')
 
    authorContext = Author.objects.get(id=request.user)


    try:
        authorContext.firstname = editForm.cleaned_data['firstname']
        authorContext.lastname = editForm.cleaned_data['lastname']
        authorContext.phone = editForm.cleaned_data['phone']
        authorContext.dob = editForm.cleaned_data['dob']
        authorContext.gender = editForm.cleaned_data['gender']
        authorContext.gitURL = editForm.cleaned_data['gitURL']

        authorContext.save()

    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/author/')
