from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from .utils import can_view_post, can_view_feed
# Create your models here.


class Author(models.Model):

    genderChoices = (
        ('M', 'male'),
        ('F', 'female'),
        ('N', 'unknown')
    )

    # This references the built-in django User object
    id = models.OneToOneField(
        User,
        primary_key=True,
        max_length=32,
        on_delete=models.CASCADE
    )
    friend = models.ManyToManyField("self", related_name="friend", blank=True)
    firstname = models.TextField(blank=True)
    lastname = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=genderChoices, blank=True)
    gitURL = models.TextField(blank=True)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.id)

    def getAuthorURL(self):
        return settings.LOCAL_HOST + 'author/' + self.id.id

    def isFollowing(self, author):
        return Follow.objects.filter(
            Q(followee=author) & Q(follower=self)
        ).exists()

    def isFriend(self, author):
        return Follow.objects.filter(
            Q(followee=self) & Q(follower=author) |
            Q(followee=author) & Q(follower=self)
        ).count() == 2

    def isFriendOfFriend(self, author):
        return author in get_friends_of_friends(self)

    def canViewPost(self, post):
        return can_view_post(self, post)
    
    def canViewFeed(self, post):
        return can_view_feed(self, post)

    def followers(self):
        return get_followers(self)

    def get_friends(self):
        return get_friends(self)


class Follow(models.Model):

    follower = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="follower",
    )

    followee = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="followee"
    )

    class Meta:
        unique_together = ["follower", "followee"]


def get_friends_of_friends(author):
    fof = []
    for f in get_friends(author):
        fof += get_friends(f)
    return fof


def get_friends(author):
    return [a.follower for a in author.followers() if author.isFriend(a.follower)]


def get_followers(author):
    return Follow.objects.filter(followee=author)
