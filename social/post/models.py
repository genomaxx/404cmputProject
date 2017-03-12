from django.db import models
from author.models import Author
from django.utils import timezone
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

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    privacyLevel = models.IntegerField(choices=VISIBILITY, default=0)
    image_url = models.TextField(blank=True)
    image = models.TextField(blank=True)
    image_type = models.TextField(blank=True)


    # Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return str(self.content)
