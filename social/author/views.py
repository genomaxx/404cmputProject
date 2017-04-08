from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from author.models import Author, Follow
from post.models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from django.utils.html import escape, format_html
from django.template.loader import render_to_string
from CommonMark import commonmark

from . import forms
from .utils import get_friend_status
from node.get import create_remote_author
import sys
import base64
import uuid
import re
from node.models import Node
# Create your views here.

@login_required
def index(request):
    # This page displays the author's stream/post feed.
    # https://docs.djangoproject.com/en/1.10/topics/db/queries/
    author = Author.objects.get(id=request.user)
    context = {'author': author}
    viewablePosts = []
    get_remote_posts()
    # Get all post objects that are public and private
    # TODO: Add to the query to expand the feed.
    try:
        posts = Post.objects.all().order_by('-publishDate')
        for post in posts:
            if author.canViewFeed(post):
                post.content = get_content(post) # You should do this instead of doing double iteration
                viewablePosts.append(post)
    except:
        return HttpResponse(sys.exc_info[0])
    # Redundant iterations
    #for p in posts:
    #    p.content = get_content(p)

    try:
        if (len(posts) > 0):
            context['posts'] = viewablePosts
            return render(request, 'author/index.html', context)
    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/index.html', context)

@login_required
def ajaxposts(request):
    author = Author.objects.get(id=request.user)
    context = dict()
    html = dict()    
    viewablePosts = []
    get_remote_posts()
    # Get all post objects that are public and private
    # TODO: Add to the query to expand the feed.
    try:
        posts = Post.objects.all().order_by('-publishDate')
        for post in posts:
            if author.canViewFeed(post):
                post.content = get_content(post) # So you don't need to iterate over the same list twice
                viewablePosts.append(post)
    except:
        return HttpResponse(sys.exc_info[0])
    
    # Redundant iteration here    
    #for p in posts:
    #    p.content = get_content(p)

    try:
        if (len(posts) > 0):
            context['posts'] = viewablePosts
            html['posts'] = render_to_string('author/ajaxposts.html', context, request=request)
            return JsonResponse(html)
    except:
        return HttpResponse(sys.exc_info[0])

    return JsonResponse(html)

def get_content(post):
    if post.contentType.startswith("image"):
        return "<img class=\"img-responsive\" src=\"{}\"/>".format(post.content)
    return post.content


def get_remote_posts():
    try:
        trusted_nodes = Node.objects.filter(trusted=True)
        for n in trusted_nodes:
            n.grab_public_posts()
    except:
        pass


@login_required
def author_post(request):
    # Only process the author's post if it is a POST request
    if (request.method != 'POST'):
        return HttpResponseRedirect('/author/')

    if (request.POST['post_content'] == '' and 'image' not in request.FILES.keys()):
        return HttpResponseRedirect('/author/')

    try:
        # Get the logged in user and the associated author object.
        # userContext = User.objects.get(username=request.user.username)
        # post_body = request.POST['post_content']

        authorContext = Author.objects.get(id=request.user)

        content = request.POST['post_content']
        content = escape(content) # Should always be escaping HTML tags
        if request.POST['contentType'] == 'markdown':
            ctype = 'commonmark'
        else:
            ctype = 'plain'

        if ('image' in request.FILES.keys()):
            # Create and save a new post.
            # encode image into base64 here and make nice image url too
            imgname = re.sub('[^._0-9a-zA-Z]+','',request.FILES['image'].name)
            base64Image = base64.b64encode(request.FILES['image'].read())
            imagePost = Post(author=authorContext,
                           content=base64Image,
                           contentType=request.FILES['image'].content_type,
                           privacyLevel=request.POST['privacy_level'], 
                           image = base64Image,\
                           image_url = '{0}_{1}_{2}'.format(request.user, str(uuid.uuid4())[:8], imgname),\
                           image_type = request.FILES['image'].content_type)
            setVisibility(request, imagePost)
            imagePost.setApiID()
            imagePost.save()
            imagePost.setOrigin()
            imagePost.source = imagePost.origin
            imagePost.save()


        elif request.POST['post_content'] != '':
            #content = request.POST['post_content']
            #content = escape(content)
            newPost = Post(
                author=authorContext,
                content=content,
                privacyLevel=request.POST['privacy_level'],
                contentType=ctype
            )
            setVisibility(request, newPost)
            newPost.setApiID()
            newPost.save()
            # need django to autogenerate the ID before using it to set the origin url
            newPost.setOrigin()
            newPost.source = newPost.origin
            newPost.save()
        #priv = newPost.privacyLevel
            ''' Factored out
        if priv == '0':
            newPost.visibility = 'PUBLIC'
        elif priv == '1':
            newPost.visibility = 'FRIENDS'
        elif priv == '2':
            newPost.visibility = 'FOAF'
        elif priv == '3':
            newPost.visibility = 'PRIVATE'
        elif priv == '4':
            newPost.visibility = 'PRIVATE'
        elif priv == '5':
            newPost.visibility = 'UNLISTED'
            newPost.unlisted = True
        '''
        else:
            return HttpResponseRedirect('/author/')

        if request.POST['privacy_level'] == '5':
            redirect = '/post/' + str(newPost.id)
            return HttpResponseRedirect(redirect)

    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/author/')

def setVisibility(request, post):
    if post.privacyLevel == '0':
            post.visibility = 'PUBLIC'
    elif post.privacyLevel == '1':
            post.visibility = 'FRIENDS'
    elif post.privacyLevel == '2':
            post.visibility = 'FOAF'
    elif post.privacyLevel == '3':
            post.visibility = 'PRIVATE'
    elif post.privacyLevel == '4':
            post.visibility = 'PRIVATE'
    elif post.privacyLevel == '5':
            post.visibility = 'UNLISTED'
            post.unlisted = True
    if 'serverOnly' in request.POST:
            post.serverOnly = True

# http://stackoverflow.com/questions/3539187/serve-static-files-through-a-view-in-django
@login_required()
def author_image(request,pk,pk1):
    post = get_object_or_404(Post, id=pk, image_url= pk1)
    response = HttpResponse(content=base64.b64decode(post.image), content_type=post.image_type)
    response['Content-Disposition'] = "filename="+post.image_url
    return response


# Implementation based upon the code found here
# http://stackoverflow.com/questions/19754103/django-how-to-delete-an-object-using-a-view
@login_required
def author_delete_post(request, postpk):
    # Only process the request if it is in fact a request to delete the post

    if (request.method != 'POST'):
        return HttpResponseRedirect('/author/')

    try:
        # Get the post object that the user is trying to delete.
        the_post = Post.objects.get(id=postpk)
        user = request.user
        postauthor = the_post.author

        # Verify that the user was the author of that post
        if user.id != postauthor.id.id:
            return HttpResponseForbidden()

        # Delete the post
        the_post.delete()
    except:
        HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect("/author/" + str(user.id))


@login_required
def remote_profile(request, uuid):
    author = create_remote_author(uuid)
    return render(request, 'author/profile.html', context)


@login_required
def profile(request, id):
    # This page displays the author's profile.
    user = User.objects.get(id=id)
    author = Author.objects.get(id=user)
    context = {'author': author}
    viewer = Author.objects.get(id=request.user)
    viewablePosts = []
    visitor = Author.objects.get(id=request.user)
    context["friend_status"] = get_friend_status(author, visitor)
    context["follows"] = False
    if visitor.isFollowing(author):
        context["follows"] = True

    try:
        posts = Post.objects.filter(
            Q(author__id=author.id)
            ).order_by('-publishDate')

        for post in posts:
            if viewer.canViewFeed(post):
                post.content = get_content(post)
                viewablePosts.append(post)
    except:
        return HttpResponse(sys.exc_info[0])

    try:

       if (len(posts) > 0):
           context['posts'] = viewablePosts

    except:
        return HttpResponse(sys.exc_info[0])

    return render(request, 'author/profile.html', context)

@login_required
def ajaxprofileposts(request, id):
    # This page displays the author's profile.
    user = User.objects.get(id=id)
    author = Author.objects.get(id=user)
    context = dict()
    html = dict()
    viewer = Author.objects.get(id=request.user)
    viewablePosts = []

    try:
        posts = Post.objects.filter(
            Q(author__id=author.id)
            ).order_by('-publishDate')

        for post in posts:
            if viewer.canViewFeed(post):
                post.content = get_content(post)
                viewablePosts.append(post)
    except:
        return HttpResponse(sys.exc_info[0])

    try:
       if (len(posts) > 0):
           context['posts'] = viewablePosts
           html['posts'] = render_to_string('author/ajaxprofileposts.html', context, request=request)
           return JsonResponse(html)
    except:
        return HttpResponse(sys.exc_info[0])

    return JsonResponse(html)


@login_required
def edit(request):
    authorContext = Author.objects.get(id=request.user)
    return render(request, 'author/edit.html', {'author': authorContext})


@login_required
def edit_post(request):
    # This page edits the author's profile

    if (request.method != 'POST'):
        return HttpResponseRedirect('/edit/')

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
        authorContext.github = editForm.cleaned_data['github']
        authorContext.githubusername = editForm.cleaned_data['githubusername']

        authorContext.save()

    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/author/')


def follow(request, id):
    profile = User.objects.get(id=id)
    follower = Author.objects.get(id=request.user)
    followee = Author.objects.get(id=profile)

    Follow(follower=follower, followee=followee).save()

    if (followee.host != "http://polar-savannah-14727.herokuapp.com"):
        # do some things!! like posting a friend request to the remote server!
        host = "http://" + followee.host.strip("http://").strip("/") + "/"
        Node.objects.get(url=host).friend_request(follower, followee)

    return HttpResponseRedirect("/author/" + id)


def unfollow(request, id):
    profile = User.objects.get(id=id)
    follower = Author.objects.get(id=request.user)
    followee = Author.objects.get(id=profile)

    relation = Follow.objects.get(follower=follower, followee=followee)
    relation.delete()
    return HttpResponseRedirect("/author/" + id)


class FollowersList(View):

    def get(self, request, id):
        auth = Author.objects.get(id__id=id)
        follow_list = auth.getFriendRequests()
        context = {
            'follow_list': follow_list,
            'title': "Friend Requests",
            'author': auth,
            'none': "No friend requests"
        }
        return render(request, 'author/followers.html', context)


class FriendsList(View):

    def get(self, request, id):
        author = Author.objects.get(id__id=id)
        follow_list = author.getFriends()
        context = {
            'follow_list': follow_list,
            'title': "Friends",
            'author': author,
            'none': "You have no friends!"
        }
        return render(request, 'author/followers.html', context)
