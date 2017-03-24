from django.db import models
import urllib
import json
import uuid
from django.utils.dateparse import parse_datetime

from post.models import Post
from author.models import Author


# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    trusted = models.BooleanField()
    post_route = "/post/"

    def grab_public_posts(self):
        full_path = "http://" + self.url + self.post_route
        post_json = urllib.request.urlopen(full_path)
        post_json = json.loads(post_json)

        for i in post_json["results"]:
            build_post(i)


def build_post(post_json):
    uid = uuid.UUID(post_json["UID"])
    post, _ = Post.objects.get_or_create(UID=uid)

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
    post.author = Author.objects.all()[0]

    post.save()
