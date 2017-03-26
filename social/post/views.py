from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views import View
from django.db.models import Q

from post.models import Post
from post.forms import CommentForm
from comment.models import Comment
from author.models import Author


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
            comment = Comment(
                content=form.cleaned_data['content'],
                author=comment_author,
                post=Post.objects.get(id=pk)
            )
            comment.setApiID()
            comment.save()

        return HttpResponseRedirect("/post/" + pk)
