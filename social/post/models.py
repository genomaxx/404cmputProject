from django.db import models
from author.models import Author
from django.conf import settings
from django.utils import timezone
import uuid;
# Create your models here.

class Post(models.Model):
    VISIBILITY = [
        (0, 'Public'),
        (1, 'Friends'),
        (2, 'Friends of friends'),
        (3, 'Private message'),
        (4, 'Private'),
        (5, 'Unlisted'),
    ]

    CONTENT_TYPE = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    privacyLevel = models.IntegerField(choices=VISIBILITY, default=0)
    image_url = models.TextField(blank=True)
    image = models.TextField(blank=True)
    image_type = models.TextField(blank=True)

    # NEW API FIELDS (You might want to integrate these with the UI so they set properly)
    title = models.CharField(max_length=124, blank=True)
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    contentType = models.CharField(max_length=128, choices=CONTENT_TYPE, default='text/plain')
    description = models.CharField(max_length=64, blank=True)
    categories = models.CharField(max_length=128, blank=True)
    unlisted = models.BooleanField(default=False)
    UID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return str(self.content)

    def setOrigin(self):
        self.origin = str(settings.LOCAL_HOST) + 'post/' + str(self.id)

    def checkIfPostShouldBeUnlisted(self):
        if (self.privacyLevel == 5):
            self.unlisted = True
