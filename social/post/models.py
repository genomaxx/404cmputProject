from django.db import models
from author.models import Author
from django.utils import timezone
import uuid
# Create your models here.

class Post(models.Model):
    VISIBILITY = [
        (0, 'Public'),
        (1, 'Friends'),
        (2, 'Friends of friends')
        (3, 'Private message'),
        (4, 'Private')
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True)
    author = models.ForeignKey(Author, on_delete=Cascade)
    content = models.TextField()
    privacyLevel = models.IntegerField(choices=VISIBILITY, default=0)

    #Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.content