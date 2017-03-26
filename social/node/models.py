from django.db import models
import json
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
import requests
import sys

from post.models import Post
from author.models import Author


# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    trusted = models.BooleanField()
    post_route = "posts/"

    def grab_public_posts(self):
        full_path = self.url + self.post_route
        response = self.make_request(full_path)
        post_json = json.loads(response)

        for i in post_json["posts"]:
            build_post(i)

    def make_request(self, url):
        sys.stderr.write(self.user)
        sys.stderr.write(self.password)
        return requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(
                self.user,
                self.password
            )
        ).text


def build_post(post_json):
    uid = uuid.UUID(post_json["id"])

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
    post.publishDate = parse_datetime(post_json["published"])

    post.save()


def build_author(author_json):
    uid = uuid.UUID(author_json["id"])

    user, _ = User.objects.get_or_create(username=author_json["id"])

    author, _ = Author.objects.get_or_create(id=user, UID=uid)

    author.displayName = author_json["displayName"]
    author.host = author_json["host"]
    author.url = author_json["url"]
    author.gitURL = author_json["github"]
    author.save()

    return author
