from rest_framework import serializers
from django.contrib.auth.models import User
from post.models import Post
from author.models import Author

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AuthorSerializer(serializers.ModelSerializer):
    id = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'firstname', 'lastname', 'phone', 'dob']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    query = 'post'
    
    class Meta:
        model = Post
        fields = ['author', 'content', 'publishDate']

   