from django.db import models
from author.models import Author
from post.models import Post
from django.utils import timezone


# Create your models here.
class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()

    # Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return str(self.content)
