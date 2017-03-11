from django.db import models
from author.models import Author
from django.utils import timezone
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user id>/<post id>_<filename>
    return '{0}/{1}_{2}'.format(instance.author.id, instance.id, filename)


class Post(models.Model):
    VISIBILITY = [
        (0, 'Public'),
        (1, 'Friends'),
        (2, 'Friends of friends'),
        (3, 'Private message'),
        (4, 'Private'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    privacyLevel = models.IntegerField(choices=VISIBILITY, default=0)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    # Audit fields
    publishDate = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return str(self.content)
