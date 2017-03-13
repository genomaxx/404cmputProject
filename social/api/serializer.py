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
    class Meta:
        model = Author
        fields = ['UID',
                  'displayName',
                  'host',
                  'url']

class AuthorSerializer(serializers.ModelSerializer):
    friend = FriendSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['UID',
                  'displayName',
                  'host',
                  'url',
                  'gitURL',
                  'friend']

    # Override method
    # http://stackoverflow.com/questions/37985581/how-to-dynamically-remove-fields-from-serializer-output
    # http://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
    def to_representation(self, authObj):
        rep = super(AuthorSerializer, self).to_representation(authObj)

        # Friends do not need to show up if it is not a profile request
        if (self.context != 'profile'):
            rep.pop('friend')

        return rep

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
    size = serializers.SerializerMethodField('add_page_size')

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
                  'size',
                  'count',
                  'comments']
    
    def add_comments(self, postObj):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query = Comment.objects.filter(post=postObj).order_by('-publishDate')
        paginated = paginator.paginate_queryset(query, self.context)
        response = CommentSerializer(paginated, many=True)
        return response.data
     
    def count_comments(self, postObj):
        query = Comment.objects.filter(post=postObj)
        return (len(query))

    def add_page_size(self, postObj):
        if ('size' not in self.context.GET):
            return 20;
        return self.context.GET['size']
        
   