from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
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
