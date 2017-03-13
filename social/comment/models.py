from django.db import models
from author.models import Author
from post.models import Post
from django.utils import timezone
import uuid


# Create your models here.
class Comment(models.Model):
    CONTENT_TYPE = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()

    # For API
    # TODO: Add the option to add content type to when making a comment
    UID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contentType = models.CharField(max_length=128, choices=CONTENT_TYPE, default='text/plain')
    # Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return str(self.content)
