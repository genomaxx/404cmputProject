from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Author(models.Model):

    genderChoices = (
        ('M', 'male'),
        ('F', 'female')
    )

    id = models.OneToOneField(User, primary_key=True, max_length=32, on_delete=models.CASCADE) # This references the built-in django User object
    friend = models.ManyToManyField("self", related_name="friend", blank=True)
    phone = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=genderChoices, blank=True)
    gitURL = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.id)

    def getAuthorURL(self):
        return settings.LOCAL_HOST + 'a/' + self.id
