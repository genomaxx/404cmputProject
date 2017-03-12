from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from post.models import Post
from author.models import Author
from comment.models import Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['UID',
                  'displayName',
                  'host',
                  'url',
                  'gitURL']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['UID',
                  'author',
                  'content',
                  'contentType', 
                  'publishDate']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    query = 'post'
    comments = serializers.SerializerMethodField('add_comments')
    count = serializers.SerializerMethodField('count_comments')

    class Meta:
        model = Post
        fields = ['UID',
                  'title',
                  'source',
                  'origin',
                  'content',
                  'contentType',
                  'description',
                  'author',
                  'categories',
                  'unlisted',
                  'publishDate',
                  'comments',
                  'count']
    
    def add_comments(self, postObj):
        paginator = PageNumberPagination(page_size=5)
        query = Comment.objects.filter(post=postObj).order_by('-publishDate')
        paginated = paginator.paginate_queryset(query, self.context['request'])
        if (len(query) <= 1):
                response = CommentSerializer(paginated, context={'request': self.context['request']})
                return response.data
        response = CommentSerializer(paginated, many=True, context={'request': self.context['request']})
        return response.data
     
    def count_comments(self, postObj):
        query = Comment.objects.filter(post=postObj)
        return (len(query))
        
   