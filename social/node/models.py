from django.db import models
import simplejson as json
import uuid
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
import requests
import sys

from post.models import Post
from author.models import Author
from comment.models import Comment
from django.conf import settings


# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    trusted = models.BooleanField()

    user = models.OneToOneField(
        User,
        max_length=32,
        on_delete=models.CASCADE
    )

    post_route = "author/posts/"
    friends_route = "author/{}/friends/"
    friend_request_route = "friendrequest/"

    PRIVACY = {
        "PUBLIC": 0,
        "FRIENDS": 1,
        "FOAF": 2,
        "PRIVATE": 3
    }

    def get_author(self, url):
        response = json.loads(self.make_request(url))
        author = build_author(response)
        return author

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
                self.username,
                self.password
            )
        ).text

    def build_post(self, post_json):
        uid = uuid.UUID(post_json["id"])

        author = self.add_author_and_friends(post_json["author"])
        post, _ = Post.objects.get_or_create(UID=uid, author=author)

        post.apiID = post_json["id"]
        post.UID = uid
        post.content = post_json["content"]
        post.title = post_json["title"]
        post.source = post_json["source"]
        post.origin = post_json["origin"]
        post.privacyLevel = self.PRIVACY[post_json["visibility"]]
        post.visibility = post_json["visibility"]
        post.contentType = post_json["contentType"]
        post.description = post_json["description"]
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

        sys.stderr.write(str(friend_json))

        for f in friend_json["authors"]:
            author_json = json.loads(self.make_request(f))
            build_author(author_json)

    def friend_request(self, follower, followee):
        data = {
            "query": "friendrequest",
            "author": {
                "id": follower.apiID,
                "host": follower.host,
                "displayName": follower.displayName,
                "url": follower.url
            },
            "friend": {
                "id": followee.apiID,
                "host": followee.host,
                "displayName": followee.displayName,
                "url": followee.url

            }
        }

        request_url = self.url + self.friend_request_route

        sys.stderr.write("Sending friend request!\n")
        sys.stderr.write(str(json.dumps(data)) + "\n")

        r = requests.post(
            url=request_url,
            data=json.dumps(data),
            auth=requests.auth.HTTPBasicAuth(
                self.username,
                self.password
            ),
            headers={
                "content-type": "application/json"
            }
        )

        sys.stderr.write(r.text + "\n")

    def __str__(self):
        return self.url


def build_author(author_json):
    author, _ = build_author_maybe(author_json)
    return author


def build_author_maybe(author_json):
    id = build_id(author_json["id"])
    uid = uuid.UUID(id)

    user = None
    if not author_json["host"].startswith(settings.APP_URL):
        user, created = User.objects.get_or_create(username=str(uid))
    else:
        created = False
        user = User.objects.get(username=author_json["displayName"])

    author, _ = Author.objects.get_or_create(id=user, UID=uid)

    # In the case of a foreign author associate that author with its node.
    if not author_json["host"].startswith(settings.APP_URL):
        author.node = Node.objects.get(url = author_json["host"])
        
    author.displayName = author_json["displayName"]
    author.host = author_json["host"]
    author.url = author_json["url"]
    author.apiID = author_json["id"]
    # author.gitURL = author_json["github"]
    # sys.stderr.write(author.apiID)
    author.save()

    return author, created


def build_id(author_url):
    return author_url.strip("/").split("/")[-1]


def build_comment(comment_json, postObj):
    # commented out for T5 atm
    # uid = uuid.UUID(comment_json['guid'])

    uid = uuid.UUID(comment_json['id'])

    authorObj = build_author(comment_json['author'])

    comment, _ = Comment.objects.get_or_create(
        UID=uid,
        post=postObj,
        author=authorObj
    )

    comment.content = comment_json['comment']
    comment.contentType = comment_json['contentType']
    comment.publishDate = comment_json['published']
    comment.apiID = comment_json['id']
    comment.save()
