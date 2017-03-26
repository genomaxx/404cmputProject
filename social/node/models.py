from django.db import models
import urllib
import json
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User

from post.models import Post
from author.models import Author
from comment.models import Comment

# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    trusted = models.BooleanField()
    post_route = "api/post/"

    def grab_public_posts(self):
        full_path = self.url + self.post_route
        post_json = urllib.request.urlopen(full_path).read()
        post_json = json.loads(post_json)

        for i in post_json["results"]:
            build_post(i)


def build_post(post_json):
    uid = uuid.UUID(post_json["UID"])

    author = build_author(post_json["author"])
    post, _ = Post.objects.get_or_create(UID=uid, author=author)

    post.content = post_json["content"]
    post.title = post_json["title"]
    post.source = post_json["source"]
    post.origin = post_json["origin"]
    post.privacyLevel = 0
    post.contentType = post_json["contentType"]
    post.description = post_json["description"]
    post.categories = post_json["categories"]
    post.unlisted = post_json["unlisted"]
    post.publishDate = parse_datetime(post_json["publishDate"])

    post.save()


def build_author(author_json):
    uid = uuid.UUID(author_json["id"])

    user, _ = User.objects.get_or_create(username=author_json["displayName"])

    author, _ = Author.objects.get_or_create(id=user, UID=uid)

    author.displayName = author_json["displayName"]
    author.host = author_json["host"]
    author.url = author_json["url"]
    author.gitURL = author_json["github"]
    author.save()

    return author

def build_comment(comment_json, postObj):
    uid = uuid.UUID(comment_json['guid'])
    authorObj = build_author(comment_json['author'])
    comment, _ = Comment.objects.get_or_create(UID=uid, post=postObj, author=authorObj)
    comment.content = comment_json['comment']
    comment.contentType = comment_json['contentType']
    comment.publishDate = comment_json['published']
    comment.setApiID
    comment.save()