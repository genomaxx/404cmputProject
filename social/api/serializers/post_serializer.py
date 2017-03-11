from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'content', 'privacyLevel', 'publishDate')