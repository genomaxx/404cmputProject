from django.db import models
import json
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
import requests
import sys

from post.models import Post
from author.models import Author
from comment.models import Comment


# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    trusted = models.BooleanField()

    post_route = "posts/"
    friends_route = "author/{}/friends/"
    friend_request_route = "friendrequest/"

    PRIVACY = {
        "PUBLIC": 0,
        "FRIENDS": 1,
        "FOAF": 2,
        "PRIVATE": 3,
        "SERVERONLY": 5
    }

    def grab_public_posts(self):
        full_path = self.url + self.post_route
        response = self.make_request(full_path)
        post_json = json.loads(response)

        for i in post_json["posts"]:
            self.build_post(i)

    def make_request(self, url):
        return requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(
                self.user,
                self.password
            )
        ).text

    def build_post(self, post_json):
        uid = uuid.UUID(post_json["id"])

        author = self.add_author_and_friends(post_json["author"])
        post, _ = Post.objects.get_or_create(UID=uid, author=author)

        post.content = post_json["content"]
        post.title = post_json["title"]
        post.source = post_json["source"]
        post.origin = post_json["origin"]
        post.privacyLevel = self.PRIVACY[post_json["visibility"]]
        post.contentType = post_json["contentType"]
        post.description = post_json["description"]
        post.categories = post_json["categories"]
        post.unlisted = post_json["unlisted"]
        post.publishDate = parse_datetime(post_json["published"])

        post.save()

    def add_author_and_friends(self, author_json):
        author, created = build_author_maybe(author_json)

        if created:
            self.add_friends(author)

        return author

    def add_friends(self, author):
        friend_path = self.url + self.friends_route.format(author.UID)
        friend_json = json.loads(self.make_request(friend_path))

        for f in friend_json["friends"]:
            author_json = json.loads(self.make_request(f))
            build_author(author_json)

    def friend_request(self, follower, followee):
        data = {
            "author": {
                "id": str(follower.UID).replace("-", ""),
                "host": follower.host,
                "displayName": follower.displayName,
                "url": follower.url
            },
            "friend": {
                "id": str(follower.UID).replace("-", ""),
                "host": followee.host,
                "displayName": followee.displayName,
                "url": followee.url

            }
        }
        request_url = self.url + self.friend_request_route

        sys.stderr.write("Sending friend request!\n")
        sys.stderr.write(str(data) + "\n")

        r = requests.post(request_url, data)

        sys.stderr.write(r.text + "\n")


def build_author(author_json):
    author, _ = build_author_maybe(author_json)
    return author


def build_author_maybe(author_json):
    uid = uuid.UUID(author_json["id"])

    user, created = User.objects.get_or_create(username=author_json["id"])

    author, _ = Author.objects.get_or_create(id=user, UID=uid)
    author.displayName = author_json["displayName"]
    author.host = author_json["host"]
    author.url = author_json["url"]
    author.gitURL = author_json["github"]
    author.save()

    return author, created


def build_comment(comment_json, postObj):
    uid = uuid.UUID(comment_json['guid'])
    authorObj = build_author(comment_json['author'])
    comment, _ = Comment.objects.get_or_create(UID=uid, post=postObj, author=authorObj)
    comment.content = comment_json['comment']
    comment.contentType = comment_json['contentType']
    comment.publishDate = comment_json['published']
    comment.setApiID
    comment.save()
