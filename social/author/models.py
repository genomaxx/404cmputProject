from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
# Create your models here.

class Author(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True) # Use this as a separate ID for the author
    user = models.OneToOneField(User, primary_key=True, max_length=32) # This references the built-in django User object
    friend = models.ManyToManyField("self", related_name="friend", blank=True)
    
    def __str__(self):
        return self.id

    def getAuthorURL(self):
        return settings.LOCAL_HOST + 'a/' + self.id
