from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import DetailView
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

import sys


from post.models import Post
from post.forms import CommentForm
from comment.models import Comment
from author.models import Author
from node.models import Node, build_comment

from urllib.parse import urlparse
import simplejson as json
import requests
import re
import base64
import uuid
from CommonMark import commonmark

APP_URL = settings.APP_URL

@login_required
def EditView(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.contentType.startswith("image"):
        base64image = post.content
        post.content = "<img alt=\"{}\" class=\"img-responsive\" src=\"{}\"/>".format(post.title,base64image)
    authorContext = Author.objects.get(id=request.user)
    if authorContext != post.author:
        return HttpResponseRedirect('/post/{}/'.format(pk))
    return render(request, 'edit.html', {'post':post})
    
@login_required
def EditPostView(request, pk):
    # Only process the author's post if it is a POST request
    if (request.method != 'POST'):
        return HttpResponseRedirect('/post/{}/edit/'.format(pk))

    if (request.POST['post_content'] == '' and 'image' not in request.FILES.keys()):
        return HttpResponseRedirect('/post/{}/edit/'.format(pk))

    try:
        # Get the logged in user and the associated author object.
        # userContext = User.objects.get(username=request.user.username)
        # post_body = request.POST['post_content']

        authorContext = Author.objects.get(id=request.user)
        post = get_object_or_404(Post, id=pk)
        
        if authorContext != post.author:
            return HttpResponseRedirect('/post/{}/'.format(pk))

        content = request.POST['post_content']
        content = escape(content) # Should always be escaping HTML tags

        if post.contentType.startswith("image"):
            # Create and save a new post.
            # encode image into base64 here and make nice image url too
            if ('image' in request.FILES.keys()):
                imgname = re.sub('[^._0-9a-zA-Z]+','',request.FILES['image'].name)
                base64Image = base64.b64encode(request.FILES['image'].read())
                post.content='data:' + str(post.contentType) + ',' + str(base64Image.decode('utf-8'))
                post.contentType=request.FILES['image'].content_type + ";base64"
                post.image_url = '{0}_{1}_{2}'.format(request.user, str(uuid.uuid4())[:8], imgname)
            post.privacyLevel=request.POST['privacy_level']
            setVisibility(request, post)
            post.save()


        elif request.POST['post_content'] != '':
            #content = request.POST['post_content']
            #content = escape(content)
            post.content=content
            post.privacyLevel=request.POST['privacy_level']
            post.contentType=request.POST['contentType']
            setVisibility(request, post)
            post.save()
            
        else:
            return HttpResponseRedirect('/post/{}/edit/'.format(pk))

        if request.POST['privacy_level'] == '5':
            return HttpResponseRedirect('/post/{}/'.format(pk))

    except:
        return HttpResponse(sys.exc_info[0])

    return HttpResponseRedirect('/post/{}/'.format(pk))

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
    else:
        post.serverOnly = False
        

@login_required
def AjaxComments(request, pk):
    author_post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(Q(post=author_post.id)).order_by('-publishDate')
    
    parsed_post_url = urlparse(author_post.origin)
    parsed_app_url = urlparse(APP_URL)
    
    if parsed_post_url.netloc != parsed_app_url.netloc:
        comment_ids = comments.values_list('UID',flat = True)
        comment_ids = [str(x) for x in comment_ids]
        
        host = "http://"+parsed_post_url.netloc + "/"
                
        n = Node.objects.get(url=host)
        
        r = requests.get(author_post.origin + "comments" +"/", auth = requests.auth.HTTPBasicAuth(n.username,n.password))
        
        if r.status_code == requests.codes.ok:
            post_objects = json.loads(r.text)
            for o in post_objects['comments']:
                if o['id'] not in comment_ids:
                    build_comment(o, author_post)
            
            # get the new comments
            comments = Comment.objects.filter(Q(post=author_post.id)).order_by('-publishDate')

    context = dict()
    html = dict()    
    context['comment_list'] = comments
    html['comments'] = render_to_string('ajaxcomments.html', context, request=request)       
    return JsonResponse(html)

# Create your views here.
class PostView(DetailView):
    model = Post
    template_name = 'view.html'      

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_list'] = self.get_comment_list()
        context['form'] = CommentForm()
        context['content'] = self.get_content()
        return context

    def get_comment_list(self):
        author_post = self.get_object()
        comments = Comment.objects.filter(Q(post=author_post.id)).order_by('-publishDate')
        
        parsed_post_url = urlparse(author_post.origin)
        parsed_app_url = urlparse(APP_URL)
        
        if parsed_post_url.netloc != parsed_app_url.netloc:
            comment_ids = comments.values_list('UID',flat = True)
            comment_ids = [str(x) for x in comment_ids]
            
            host = "http://"+parsed_post_url.netloc + "/"
                    
            n = Node.objects.get(url=host)
            
            r = requests.get(author_post.origin + "comments" +"/", auth = requests.auth.HTTPBasicAuth(n.username,n.password))
            
            if r.status_code == requests.codes.ok:
                post_objects = json.loads(r.text)
                for o in post_objects['comments']:
                    if o['id'] not in comment_ids:
                        build_comment(o, author_post)
                
                # get the new comments
                comments = Comment.objects.filter(Q(post=author_post.id)).order_by('-publishDate')
                return comments
                
            elif r.status_code == requests.codes.forbidden:
                # can't retrieve posts, just return servers post
                return comments
            else:
                # can't retrieve posts, just return servers post
                return comments

        return comments

    def dispatch(self, request, *args, **kwargs):
        author = Author.objects.get(id=request.user)
        if author.canViewPost(self.get_object()):
            return super(DetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/author/")

    def get_content(self):
        if self.object.contentType.startswith("image"):
            base64image = self.object.content
            return "<img alt=\"{}\" class=\"img-responsive\" src=\"{}\"/>".format(self.object.title,base64image)

        if self.object.contentType == 'text/markdown':
            return commonmark(self.object.content)

        return self.object.content

class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_author = Author.objects.get(id=request.user)
            comment_post = Post.objects.get(id=pk)
            
            comment = Comment(
            content=form.cleaned_data['content'],
            author=comment_author,
            post=comment_post,
            )
            comment.setApiID()

            parsed_comment_url = urlparse(comment_post.origin)
            parsed_app_url = urlparse(APP_URL)

            if parsed_comment_url.netloc == parsed_app_url.netloc:
                # post is on server, proceed as normal
                comment.save()
                return HttpResponseRedirect("/post/" + pk)
            
            else:
                # we gotta send a request and see if it's successful
                body = dict()
                body['query'] = "addComment"
                body['post'] = comment_post.origin
                obj_author = dict()
                obj_author['id'] = str(comment_author.UID)
                obj_author['host'] = comment_author.host
                obj_author['displayName'] = comment_author.displayName
                obj_author['url'] = comment_author.url
                obj_author['github'] = comment_author.github
                obj_comment = dict()
                obj_comment['author'] = obj_author
                obj_comment['comment'] = form.cleaned_data['content']
                obj_comment['contentType'] = 'text/markdown'
                obj_comment['published'] = comment.publishDate.isoformat()
                # commented out for T5 atm
                #obj_comment['guid'] = str(comment.UID)
                obj_comment['id'] = str(comment.UID)
                body['comment'] = obj_comment
                msg = json.dumps(body)
                host = "http://"+parsed_comment_url.netloc + "/"
                n = Node.objects.get(url=host)

                r = requests.post(
                    comment_post.origin + "comments" +"/",
                    data=msg,
                    auth = requests.auth.HTTPBasicAuth(n.username,n.password),
                    headers={
                        "content-type": "application/json"
                    })

                sys.stderr.write(r.text)

                if r.status_code == requests.codes.ok:
                    return HttpResponseRedirect("/post/" + pk)
                elif r.status_code == requests.codes.forbidden:
                    Comment.objects.filter(UID=comment.UID).delete()
                    return HttpResponseForbidden()
                else:
                    Comment.objects.filter(UID=comment.UID).delete()
                    return HttpResponse(r.content)

        return HttpResponseRedirect("/post/" + pk)
