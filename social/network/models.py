from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_name = models.TextField(max_length=32, blank=False)
    friends = models.ManyToManyField("self", related_name="friends", blank=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

def user_directory_path(instance, filename):
    return 'images/%s/%s_%s' % (instance.user.id, uuid.uuid4, filename)
class Image(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.ImageField(upload_to=user_directory_path)
    timestamp = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    follower = models.ForeignKey(Author, related_name="follower")
    followed = models.ForeignKey(Author, related_name="followed")
    accepted = models.NullBooleanField(default=None)
    timestamp = models.DateTimeField(auto_now=True)
