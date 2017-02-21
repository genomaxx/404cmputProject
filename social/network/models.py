from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    friends = models.ManyToManyField("self", related_name="friends", blank=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    follower = models.ForeignKey(Author, related_name="follower")
    followed = models.ForeignKey(Author, related_name="followed")
    accepted = models.NullBooleanField(default=None)
    timestamp = models.DateTimeField(auto_now=True)
