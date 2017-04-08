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

class FriendSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='apiID')

    class Meta:
        model = Author
        fields = ['id',
                  'host',
                  'displayName',
                  'url']

class AuthorSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField('add_friends')
    id = serializers.CharField(source='apiID')

    class Meta:
        model = Author
        fields = ['id',
                  'host',
                  'displayName',
                  'url',
                  'github',
                  'friends']

    def add_friends(self, postObj):
        query = postObj.get_all_following()
        response = FriendSerializer(query, many=True)
        return response.data

class CommentSerializer(serializers.ModelSerializer):
    author = FriendSerializer(read_only=True)
    comment = serializers.CharField(source='content')
    id = serializers.CharField(source='apiID')
    published = serializers.CharField(source='publishDate')

    class Meta:
        model = Comment
        fields = ['id',
                  'author',
                  'comment',
                  'contentType',
                  'published']

class PostSerializer(serializers.ModelSerializer):
    author = FriendSerializer(read_only=True)
    query = 'post'
    comments = serializers.SerializerMethodField('add_comments')
    categories = serializers.SerializerMethodField('add_categories')
    count = serializers.SerializerMethodField('count_comments')
    size = serializers.SerializerMethodField('add_page_size')
    id = serializers.CharField(source='apiID')
    published = serializers.CharField(source='publishDate')


    class Meta:
        model = Post
        fields = ['id',
                  'title',
                  'source',
                  'origin',
                  'content',
                  'contentType',
                  'description',
                  'author',
                  'categories',
                  'unlisted',
                  'published',
                  'size',
                  'count',
                  'comments',
                  'visibility']

    def add_comments(self, postObj):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query = Comment.objects.filter(post=postObj).order_by('-publishDate')
        paginated = paginator.paginate_queryset(query, self.context)
        response = CommentSerializer(paginated, many=True)
        return response.data

    def add_categories(self, postObj):
        return []

    def count_comments(self, postObj):
        query = Comment.objects.filter(post=postObj)
        return (len(query))

    def add_page_size(self, postObj):
        if ('size' not in self.context.GET):
            return 20;
        return self.context.GET['size']
