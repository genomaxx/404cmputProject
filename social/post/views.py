from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView
from django.views import View
from django.db.models import Q
from django.conf import settings

from post.models import Post
from post.forms import CommentForm
from comment.models import Comment
from author.models import Author
from node.models import Node

from urllib.parse import urlparse
import json
import requests

APP_URL = settings.APP_URL

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
        comments = Comment.objects.filter(
            Q(post=self.get_object().id)
        ).order_by('-publishDate')
        return comments

    def dispatch(self, request, *args, **kwargs):
        author = Author.objects.get(id=request.user)
        if author.canViewPost(self.get_object()):
            return super(DetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/author/")

    def get_content(self):
        if self.object.is_image():
            return self.build_image()
        return self.object.content

    def build_image(self):
        content = self.object.content
        return "<img src=\"{}\"/>".format(content)


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
            comment.save()
            
            parsed_comment_url = urlparse(comment_post.origin)
            parsed_app_url = urlparse(APP_URL)
            
            if parsed_comment_url.netloc == parsed_app_url.netloc:
                # post is on server, proceed as normal
                return HttpResponseRedirect("/post/" + pk)
            
            else:
                # we gotta send a request and see if it's successful
                body = dict()
                body['query'] = "addComment"
                body['post'] = comment_post.origin
                obj_author = dict()
                obj_author['id'] = comment_author.url
                obj_author['host'] = comment_author.host
                obj_author['displayName'] = comment_author.displayName
                obj_author['url'] = comment_author.url
                obj_author['github'] = comment_author.github
                obj_comment = dict()
                obj_comment['author'] = obj_author
                obj_comment['comment'] = form.cleaned_data['content']
                obj_comment['contentType'] = 'text/markdown'
                obj_comment['published'] = comment.publishDate.isoformat()
                obj_comment['guid'] = str(comment.UID)
                body['comment'] = obj_comment
                msg = json.dumps(body)
                
                host = "http://"+parsed_comment_url.netloc + "/"
                
                n = Node.objects.get(url=host)
                
                r = requests.post(comment_post.origin + "comments", msg, auth = requests.auth.HTTPBasicAuth(n.username,n.password))
                
                if r.status_code == request.codes.ok:
                    return HttpResponseRedirect("/post/" + pk)
                elif r.status_code == request.codes.forbidden:
                    Comment.objects.filter(UID=comment.UID).delete()
                    return HttpResponseForbidden()
                else:
                    return HttpResponse('<h1>Unknown Error Ocurred</h1>')
                    
        return HttpResponseRedirect("/post/" + pk)
